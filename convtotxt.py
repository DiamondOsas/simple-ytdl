import os
import textwrap
from bs4 import BeautifulSoup

# Define the target directory
docs_dir = "docs"

# Look at all files in the docs folder
if os.path.exists(docs_dir):
    for filename in os.listdir(docs_dir):
        file_path = os.path.join(docs_dir, filename)
        
        # We only want to process files (skip directories)
        if os.path.isfile(file_path):
            try:
                # Read the content
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                
                # If it's an HTML file, use BeautifulSoup to extract text
                if filename.lower().endswith(".html") or filename.lower().endswith(".htm"):
                    soup = BeautifulSoup(content, "html.parser")
                    clean_text = soup.get_text(separator=" ")
                else:
                    # For other files (like .txt), just use the content
                    clean_text = content

                # Minify: split into words and join with a single space
                minified_text = " ".join(clean_text.split())
                
                # Wrap text to 100 characters per line
                wrapped_text = textwrap.fill(minified_text, width=100)

                # Save as a .txt file with the same base name
                base_name = os.path.splitext(filename)[0]
                new_name = base_name + ".txt"
                new_path = os.path.join(docs_dir, new_name)

                # Overwrite if already exists
                with open(new_path, "w", encoding="utf-8") as f:
                    f.write(wrapped_text)
                    
                print(f"Processed: {filename} -> {new_name}")
                
                # Delete the original file ONLY if the name changed (e.g. .html -> .txt)
                # If we processed a .txt file, new_path is the same as file_path, so don't delete.
                if os.path.abspath(file_path) != os.path.abspath(new_path):
                    os.remove(file_path)
                    print(f"Deleted original: {filename}")

            except Exception as e:
                print(f"Error processing {filename}: {e}")
else:
    print(f"Directory '{docs_dir}' not found.")