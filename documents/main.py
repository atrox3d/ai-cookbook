from pathlib import Path
import requests
from docling.document_converter import DocumentConverter

from openai_client import get_client


PDF_URL = 'https://arxiv.org/pdf/2408.09869'
DATA_DIR = 'data'

Path(DATA_DIR).mkdir(exist_ok=True)

def convert(pdf_path:str):
    converter = DocumentConverter()

    result = converter.convert(pdf_path)
    document = result.document
    markdown_out = document.export_to_markdown()
    json_out = document.export_to_dict()

    return json_out

def get_filename_from_url(url):
    path = Path(url)
    if path.suffix:
        return path.name
    else:
        return "document.pdf"

def download_pdf(url:str, data_dir:str=DATA_DIR):
    response = requests.get(url)
    print(response.status_code)

    # if response.status_code == 200:
    response.raise_for_status()
    filename = get_filename_from_url(url)
    pdf_path = Path(data_dir) / filename
    with open(pdf_path, 'wb') as f:
        f.write(response.content)

def main():
    local_path = Path(DATA_DIR, get_filename_from_url(PDF_URL))
    if not local_path.exists():
        download_pdf(PDF_URL, DATA_DIR)

    json_out = convert(local_path)

    print(json_out)
