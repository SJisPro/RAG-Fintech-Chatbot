# backend/load_documents.py
from backend.vector_store import add_document
import os
import pandas as pd

def load_text_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

def load_csv_file(filepath):
    df = pd.read_csv(filepath)
    return df.to_string()

def load_documents_from_folder(base_path="./backend/data"):
    roles = os.listdir(base_path)
    for role in roles:
        role_path = os.path.join(base_path, role)
        if os.path.isdir(role_path):
            files = os.listdir(role_path)
            for idx, file in enumerate(files):
                filepath = os.path.join(role_path, file)
                if file.endswith('.csv'):
                    content = load_csv_file(filepath)
                else:
                    content = load_text_file(filepath)
                
                add_document(
                    doc_id=f"{role}_{idx}",
                    content=content,
                    metadata={"category": role, "source": file}
                )
                print(f"Loaded: {file} under {role}")

if __name__ == "__main__":
    load_documents_from_folder()
