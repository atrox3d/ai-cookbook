from pathlib import Path
import requests

from openai_client import get_client


PDF_URL = 'https://arxiv.org/pdf/2408.09869'
DATA_DIR = 'data'

Path(DATA_DIR).mkdir(exist_ok=True)


