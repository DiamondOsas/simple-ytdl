import os
from bs4 import BeautifulSoup

# Look at all files in the current folder

for filename in os.listdir("C:\PROGRAMMING\simple-ytdl"):
    if filename.endswith(".html"):
        with open(filename, "r", encoding="utf-8") as f:
            # Parse the HTML and extract text
            soup = BeautifulSoup(f, "html.parser")
            clean_text = soup.get_text(separator="\n")

        # Save as a .txt file with the same name
        new_name = filename.replace(".html", ".txt")
        with open(new_name, "w", encoding="utf-8") as f:
            f.write(clean_text)
            
        print(f"Converted: {filename} -> {new_name}")