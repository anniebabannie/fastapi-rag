from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import List, Dict
import time

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_embeddings(chunks: List[Dict[str, str]]) -> List[Dict]:
    """
    Generate embeddings for text chunks using OpenAI's text-embedding-ada-002 model
    
    Args:
        chunks: List of dictionaries containing text chunks and their metadata
        
    Returns:
        List of dictionaries with the original metadata plus embeddings
    """
    results = []
    
    for chunk in chunks:
        text_content = chunk['content']
        
        # Get embedding from OpenAI
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=text_content
        )
        
        # Add the embedding to the chunk data
        chunk_with_embedding = {
            'embedding': response.data[0].embedding,
            'content': text_content
        }
        
        # Optionally include 'fileName' if it exists
        if 'fileName' in chunk:
            chunk_with_embedding['fileName'] = chunk['fileName']

        results.append(chunk_with_embedding)
        
        # Add a delay to ensure no more than 100 requests per minute
        time.sleep(0.6)  # 60 seconds / 100 requests = 0.6 seconds per request

    return results

def create_embedding_from_text(text):
    # Placeholder for the actual embedding creation logic
    # This should interact with the OpenAI API or any other embedding service
    return [0.0] * 768  # Example: return a dummy embedding vector

if __name__ == "__main__":
    # Test with a sample chunk
    test_chunks = [{
        'text': 'This is a test chunk',
        'fileName': 'test.md'
    }]
    embeddings = get_embeddings(test_chunks)
    print(f"Generated embedding with length: {len(embeddings[0]['embedding'])}") 