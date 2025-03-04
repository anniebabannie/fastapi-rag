import os

def get_all_files(directory: str):
    """Get all files in a directory."""
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

def create_output_directory(input_path: str, input_base_dir: str, output_base_dir: str):
    """Create the output directory structure."""
    relative_path = os.path.relpath(input_path, input_base_dir)
    output_dir = os.path.join(output_base_dir, os.path.dirname(relative_path))
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def parse_markdown_file(file_path: str) -> str:
    """Parse and clean up a markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Add any specific markdown cleanup logic here
    return content

def main():
    """Process markdown files from fly-blog to content/blog directory."""
    input_dir = "fly-blog"
    output_base_dir = "backend/content/blog"
    
    # Ensure output directory exists
    os.makedirs(output_base_dir, exist_ok=True)
    
    # Get all files
    all_files = get_all_files(input_dir)
    print(f"Found {len(all_files)} total files in {input_dir}")
    print("All files found:", all_files)
    
    for input_path in all_files:
        if input_path.endswith(('.html.markerb', '.html.md')):
            print(f"Processing markdown file: {input_path}")
            
            # Create output directory and determine output file path
            output_dir = create_output_directory(input_path, input_dir, output_base_dir)
            output_file = os.path.basename(input_path)
            output_file = output_file.replace('.html.markerb', '.md').replace('.html.md', '.md')
            output_path = os.path.join(output_dir, output_file)
            
            # Process and write content
            content = parse_markdown_file(input_path)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Processed: {input_path} -> {output_path}")
        else:
            print(f"Skipping non-markdown file: {input_path}")
    
    print("\nProcessing complete!")

if __name__ == "__main__":
    main() 