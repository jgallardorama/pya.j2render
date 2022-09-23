import os

def ensure_dir(file_path):
    file_dir = os.path.dirname(file_path)
    os.makedirs(file_dir, exist_ok=True)  