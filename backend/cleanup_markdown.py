import os
import shutil
from pathlib import Path
import re

def parse_markdown_file(file_path: str) -> str:
    """Read and parse markdown files, stripping frontmatter if present."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Check for YAML frontmatter (between --- markers)
    frontmatter_pattern = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)
    match = frontmatter_pattern.match(content)
    
    if match:
        # Return content without frontmatter
        return content[match.end():]
    return content

def get_all_files(dir_path: str) -> list[str]:
    """Recursively get all files in directory, excluding specific folders."""
    ignore_dirs = {'.buildkite', '.git', '.github'}
    files = []
    
    for root, dirs, filenames in os.walk(dir_path):
        # Remove ignored directories
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        
        for filename in filenames:
            files.append(os.path.join(root, filename))
    
    return files

def create_output_directory(input_path: str, base_input_dir: str, base_output_dir: str) -> str:
    """Create output directory structure preserving relative paths."""
    rel_path = os.path.relpath(os.path.dirname(input_path), base_input_dir)
    output_dir = os.path.join(base_output_dir, rel_path)
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def main():
    """Process markdown files from fly-docs to docs directory."""
    input_dir = "fly-docs"
    output_base_dir = "docs"
    
    # Ensure output directory exists
    os.makedirs(output_base_dir, exist_ok=True)
    
    # Get all files
    all_files = get_all_files(input_dir)
    print(f"Found {len(all_files)} total files")
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