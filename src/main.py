import os, shutil

from copy_static import copy_files

source = "./static"
destination = "./public"

def main():
    print("Deleting public directory...")
    if os.path.exists(destination):
        shutil.rmtree(destination)
    copy_files(source, destination)

if __name__ == "__main__":
    main()

