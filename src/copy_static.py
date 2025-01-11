import os, shutil

def copy_files(source, destination):
    if not os.path.exists(destination):
        os.mkdir(destination)

    for filename in os.listdir(source):
        source_path = os.path.join(source, filename)
        target_path = os.path.join(destination, filename)
        print(f" * {source_path} -> {target_path}")
        if os.path.isfile(source_path):
            shutil.copy(source_path, target_path)
        else:
            copy_files(source_path, target_path)

