import os, shutil

from copy_static import copy_files
from generate_page import generate_page, generate_pages

source = "./static"
destination = "./public"
content = "./content"
template = "./template.html"

def main():
    print("Deleting public directory...")
    if os.path.exists(destination):
        shutil.rmtree(destination)

    print("Copying static files to public directory...")
    copy_files(source, destination)

    print("Generating page...")
    generate_pages(
        content,
        template,
        destination
    )

if __name__ == "__main__":
    main()

