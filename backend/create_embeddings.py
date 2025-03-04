import requests
from typing import TypedDict, List
from chunk_markdown import DocumentChunk, chunk_text
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer

class DocumentEmbedding(TypedDict):
    fileName: str
    chunkIndex: int
    content: str
    embedding: List[float]
    token_count: int

def get_embeddings(chunks: List[DocumentChunk]) -> List[DocumentEmbedding]:
    """Create embeddings for each chunk using the BAAI/bge-large-en model."""
    # Initialize the model and tokenizer
    MODEL_NAME = "BAAI/bge-large-en"
    model = SentenceTransformer(MODEL_NAME)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    
    embeddings: List[DocumentEmbedding] = []
    
    # Process all chunks at once for better efficiency
    contents = [chunk['content'] for chunk in chunks]
    batch_embeddings = model.encode(contents, normalize_embeddings=True)
    
    # Create embedding objects
    for i, chunk in enumerate(chunks):
        # Tokenize the content to count tokens
        tokens = tokenizer.encode(chunk['content'], add_special_tokens=True)
        token_count = len(tokens)
        
        embeddings.append({
            'fileName': chunk['fileName'],
            'chunkIndex': chunk['chunkIndex'],
            'content': chunk['content'],
            'embedding': batch_embeddings[i].tolist(),
            'token_count': token_count  # Add token count to the embedding
        })
        
        # Print detailed information for each chunk
        print(f"File: {chunk['fileName']}, Chunk Index: {chunk['chunkIndex']}, Token Count: {token_count}")
    
    return embeddings

def main():
    """Main function to demonstrate usage."""
    # First get chunks
    chunks = chunk_text()
    print(f"Processing {len(chunks)} chunks for embeddings...")
    
    # Create embeddings
    embeddings = get_embeddings(chunks)
    print(f"\nCreated {len(embeddings)} embeddings")
    
    # Print example of first embedding
    if embeddings:
        example = embeddings[0]
        print("\nExample embedding:")
        print(f"File: {example['fileName']}")
        print(f"Index: {example['chunkIndex']}")
        print(f"Content preview: {example['content'][:100]}...")
        print(f"Embedding dimensions: {len(example['embedding'])}")

if __name__ == "__main__":
    main() 