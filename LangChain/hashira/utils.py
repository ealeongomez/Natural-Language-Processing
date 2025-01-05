import os
import sys

import jsonlines
import yaml
from langchain.schema import Document

# -------------------------------------------------------------------------------------------
class DocsJSONLLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self):
        with jsonlines.open(self.file_path) as reader:
            documents = []
            for obj in reader:
                page_content = obj.get("text", "")
                metadata = {
                    "title": obj.get("title", ""),
                    "repo_owner": obj.get("repo_owner", ""),
                    "repo_name": obj.get("repo_name", ""),
                }
                documents.append(Document(page_content=page_content, metadata=metadata))
        return documents
    
# -------------------------------------------------------------------------------------------

def load_config():
    """
    Carga la configuración de la aplicación desde el archivo 'config.yaml'.

    Returns:
        Un diccionario con la configuración de la aplicación.
    """
    root_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(root_dir, "config.yaml")) as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

# -------------------------------------------------------------------------------------------

def get_file_path():
    """
    Obtiene la ruta al archivo de base de datos JSONL especificado en la configuración de la aplicación.

    Returns:
        La ruta al archivo de base de datos JSONL.
    """
    config = load_config()

    root_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.join(root_dir, "..")

    return os.path.join(parent_dir, config["jsonl_database_path"])

# -------------------------------------------------------------------------------------------

def create_dir(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)

# -------------------------------------------------------------------------------------------

def remove_existing_file(file_path: str) -> None:
    if os.path.exists(file_path):
        os.remove(file_path)
