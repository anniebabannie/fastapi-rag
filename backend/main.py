from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
import os
from pinecone import Pinecone
from dotenv import load_dotenv
import anthropic
from create_embeddings_openai import get_embeddings  # Import the OpenAI embedding function

# Load environment variables
load_dotenv()

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
# Get the most recent index (assuming the naming convention from store_embeddings.py)
indexes = [idx for idx in pc.list_indexes() if idx.name.startswith('fly-docs-')]
if indexes:
    latest_index = max(indexes, key=lambda x: int(x.name.replace('fly-docs-', '')))
    pinecone_index = pc.Index(latest_index.name)
else:
    raise ValueError("No Pinecone index found")

# Define request models
class MessageHistory(BaseModel):
    role: str
    content: str

class ChatInput(BaseModel):
    text: str
    history: List[MessageHistory]

client = anthropic.Anthropic(
    api_key=os.getenv('CLAUDE_API_KEY'),
)

async def generate_answer(context: str, conversation_history: List[dict]) -> str:
    """Generate an answer using Ollama."""

    # Format conversation history
    formatted_history = "\n".join([
        f"{'Human' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
        for msg in conversation_history
    ])
    
    # Construct the full prompt
    full_prompt = f"""You are a helpful AI assistant. Use the following documentation to help answer questions. If you don't find the answer in the documentation, say so, but then give your best guess or answer.
    

                    Documentation context:
                    {context}

                    Previous conversation:
                    {formatted_history}"""

    message = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": full_prompt}
        ]
    )

    return message

@app.post("/api/embed")
async def process_query(input: ChatInput):
    """Process a query using RAG pattern"""
    
    # 1. Generate embedding for the query using OpenAI
    query_embedding = get_embeddings([{'content': input.text}])[0]['embedding']
    
    # 2. Search Pinecone for relevant chunks
    search_results = pinecone_index.query(
        vector=query_embedding,
        top_k=3,
        include_metadata=True
    )
    
    if not search_results.matches:
        return {
            "answer": "I couldn't find relevant information in the documentation.",
            "context": []
        }
    
    # 3. Assemble the context
    context_chunks = [match.metadata['text'] for match in search_results.matches]
    context = "\n\n".join(context_chunks)
    
    # 4. Format the conversation history
    conversation_history = [
        {"role": msg.role, "content": msg.content}
        for msg in input.history
    ]
    
    # 5. Generate answer using Ollama
    answer = await generate_answer(context, conversation_history)
    
    return {
        "context": context_chunks,
        "answer": answer
    }

# Move static file mounting to the end
app.mount("/", StaticFiles(directory="dist", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
