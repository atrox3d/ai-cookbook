import os
from openai import OpenAI
from dotenv import load_dotenv



def main():
    load_dotenv()
    assert os.getenv("OPENAI_API_KEY") is not None, "OPENAI_API_KEY is not set"
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )


if __name__ == "__main__":
    main()
