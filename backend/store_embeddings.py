import os
import time
import hashlib
from typing import List
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
from create_embeddings import DocumentEmbedding

# Load environment variables
load_dotenv()

def create_chunk_id(file_name: str, chunk_index: int, content: str) -> str:
    """Create a unique ID for each chunk using MD5 hash."""
    hash_value = hashlib.md5(content.encode()).hexdigest()[:8]
    return f"{file_name}_chunk{chunk_index}_{hash_value}"

def get_next_index_name() -> str:
    """Generate the next sequential index name."""
    pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
    base_index_name = os.getenv('PINECONE_INDEX_BASE', 'fly-docs-')
    
    # List all indexes and filter for our base name
    indexes = pc.list_indexes()
    existing_numbers = [
        int(index.name.replace(base_index_name, ''))
        for index in indexes
        if index.name.startswith(base_index_name) and 
           index.name.replace(base_index_name, '').isdigit()
    ]
    
    # Get next number in sequence
    next_num = max(existing_numbers, default=0) + 1
    return f"{base_index_name}{next_num}"

def store_embeddings(embeddings: List[DocumentEmbedding]) -> None:
    """Store embeddings in a new Pinecone index."""
    if not embeddings:
        print("No embeddings to store.")
        return

    # Initialize Pinecone
    pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
    
    # Create new index with incremented name
    new_index_name = get_next_index_name()
    
    # Create the new index
    pc.create_index(
        name=new_index_name,
        dimension=len(embeddings[0]['embedding']),  # Get dimension from first embedding
        metric='cosine',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )
    
    # Wait for index to be ready
    print(f"Waiting for index {new_index_name} to be ready...")
    time.sleep(20)  # Wait 20 seconds
    
    # Connect to the new index
    index = pc.Index(new_index_name)
    
    # Store embeddings in batches
    batch_size = 100
    for i in range(0, len(embeddings), batch_size):
        batch = embeddings[i:i + batch_size]
        vectors = []
        
        for doc in batch:
            print("Document being processed:", doc)
            chunk_id = create_chunk_id(doc['fileName'], doc['chunkIndex'], doc['content'])
            vectors.append({
                'id': chunk_id,
                'values': doc['embedding'],
                'metadata': {
                    'text': doc['content'],
                    'fileName': doc['fileName'],
                    'chunkIndex': doc['chunkIndex']
                }
            })
        
        # Upsert the batch
        index.upsert(vectors=vectors)
        print(f"Stored {len(vectors)} embeddings (batch {i//batch_size + 1})")

def main(embeddings: List[DocumentEmbedding]):
    """Main function to store provided embeddings."""
    # Store embeddings in Pinecone
    store_embeddings(embeddings)
    print("Successfully stored all embeddings in Pinecone")

if __name__ == "__main__":
    # Example usage: pass embeddings to the main function
    example_embeddings = []  # Replace with actual embeddings
    main(example_embeddings) 