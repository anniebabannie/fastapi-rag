import os
import re
from typing import TypedDict, List

class DocumentChunk(TypedDict):
    fileName: str
    chunkIndex: int
    content: str

def chunk_text(docs_dir: str = 'docs', chunk_size: int = 500) -> List[DocumentChunk]:
    """Split markdown files into chunks based on sentence boundaries."""
    chunks: List[DocumentChunk] = []
    
    # Traverse the directory tree
    for root, _, files in os.walk(docs_dir):
        # Filter for markdown files
        markdown_files = [f for f in files if f.endswith('.md')]
        
        for file_name in markdown_files:
            file_path = os.path.join(root, file_name)
            
            # Compute the relative path from the docs directory
            relative_file_path = os.path.relpath(file_path, docs_dir)
            
            # Read the file content
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Split by sentences (looking for period followed by whitespace)
            sentences = re.split(r'(?<=\.)\s+', text)
            current_chunk = ""
            chunk_index = 0
            
            for sentence in sentences:
                # Check if adding this sentence would exceed chunk size
                if len(current_chunk + sentence) > chunk_size:
                    chunks.append({
                        "fileName": relative_file_path,
                        "chunkIndex": chunk_index,
                        "content": current_chunk
                    })
                    chunk_index += 1
                    current_chunk = sentence
                else:
                    # Add space between sentences if current_chunk is not empty
                    current_chunk += (" " if current_chunk else "") + sentence
            
            # Add the final chunk if there's remaining content
            if current_chunk:
                chunks.append({
                    "fileName": relative_file_path,
                    "chunkIndex": chunk_index,
                    "content": current_chunk
                })
    
    return chunks

def main():
    """Main function to demonstrate usage."""
    chunks = chunk_text()
    print(f"Created {len(chunks)} chunks from markdown files")
    
    print(len(chunks))
    # Print first few chunks as example
    for chunk in chunks:
        print("\nChunk example:")
        print(f"File: {chunk['fileName']}")
        # print(f"Index: {chunk['chunkIndex']}")
        # print(f"Content preview: {chunk['content']}")

if __name__ == "__main__":
    main() 