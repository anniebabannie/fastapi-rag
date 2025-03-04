import os

def count_markdown_files(directory: str) -> int:
    """
    Count the number of markdown files in a given directory, including subdirectories.
    
    Args:
        directory: The root directory to start the search.
        
    Returns:
        The count of markdown files.
    """
    markdown_count = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                markdown_count += 1
    return markdown_count

if __name__ == "__main__":
    docs_directory = 'backend/docs'
    num_markdown_files = count_markdown_files(docs_directory)
    print(f"Number of markdown files in '{docs_directory}': {num_markdown_files}") 