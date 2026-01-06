import os
from bs4 import BeautifulSoup

# Define the target directory
docs_dir = "docs"

# Look at all files in the docs folder
if os.path.exists(docs_dir):
    for filename in os.listdir(docs_dir):
        file_path = os.path.join(docs_dir, filename)
        
        # We only want to process files (skip directories if any)
        if os.path.isfile(file_path):
            # Determine if we should treat it as HTML or just plain text
            # The prompt asked to "convert everthing", but existing logic was for HTML.
            # We will process everything, but using BS4 is primarily for HTML.
            # If it's HTML, we strip tags. If not, we might just copy text?
            # Given the directory listing is all .html, we focus on that but handle the extension change.
            
            # Read the content
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                
                # If it's an HTML file, use BeautifulSoup to extract text
                if filename.lower().endswith(".html") or filename.lower().endswith(".htm"):
                    soup = BeautifulSoup(content, "html.parser")
                    clean_text = soup.get_text(separator="\n")
                else:
                    # For non-HTML files, just use the content as is
                    clean_text = content

                # Save as a .txt file with the same base name
                # We replace the original extension with .txt
                base_name = os.path.splitext(filename)[0]
                new_name = base_name + ".txt"
                new_path = os.path.join(docs_dir, new_name)

                with open(new_path, "w", encoding="utf-8") as f:
                    f.write(clean_text)
                    
                print(f"Converted: {filename} -> {new_name}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")
else:
    print(f"Directory '{docs_dir}' not found.")