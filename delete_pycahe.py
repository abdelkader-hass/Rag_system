import os
import shutil

def delete_pycache(directory):
    for root, dirs, _ in os.walk(directory):
        for d in dirs:
            if d == "__pycache__":
                pycache_path = os.path.join(root, d)
                shutil.rmtree(pycache_path)
                print(f"Deleted: {pycache_path}")

# Run the function in the current directory or specify a path
delete_pycache(".")
