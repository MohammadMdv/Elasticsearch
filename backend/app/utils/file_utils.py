import os
import json


def save_uploaded_file(upload_dir: str, file) -> str:
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, 'wb') as f:
        f.write(file.file.read())
    return file_path


def load_json_file(file_path: str):
    with open(file_path, 'r') as f:
        return json.load(f)
