import chunk_markdown
import create_embeddings_openai
import store_embeddings

def main():
    # First run the markdown chunking for blog content
    chunks = chunk_markdown.chunk_text(docs_dir='content/blog')
    
    # Debug: Check if chunks are being created
    if not chunks:
        print("No chunks were created.")
        return
    
    print(f"Number of chunks created: {len(chunks)}")
    
    # Then create embeddings using the OpenAI script
    embeddings = create_embeddings_openai.get_embeddings(chunks)
    
    # Debug: Check if embeddings are being created
    if not embeddings:
        print("No embeddings were created.")
        return

    # Store the embeddings in Pinecone
    store_embeddings.main(embeddings)
    
    # Print the results
    print("Generated and stored embeddings:")
    for i, embedding in enumerate(embeddings):
        print(f"Chunk {i} from {embedding['fileName']}: {embedding['embedding'][:5]}...")  # Print first 5 values
    
    return embeddings  # Return the embeddings for use by other scripts

if __name__ == "__main__":
    main() 