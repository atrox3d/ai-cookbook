# /Users/nigga/code/python/ai/openai/ai-cookbook/openai_client.py
import os
from openai import OpenAI
from dotenv import load_dotenv

def get_client() -> OpenAI:
    """
    Initializes and returns an OpenAI client.

    Raises:
        AssertionError: If the OPENAI_API_KEY environment variable is not set.

    Returns:
        OpenAI: An initialized OpenAI client.
    """
    load_dotenv()
    assert os.getenv("OPENAI_API_KEY") is not None, "OPENAI_API_KEY is not set"
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

