import os
from pydoc import cli
from openai import OpenAI
from dotenv import load_dotenv



def main():
    load_dotenv()
    assert os.getenv("OPENAI_API_KEY") is not None, "OPENAI_API_KEY is not set"
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    completion = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': 'hello, testing, testing. please reply'}
        ]
    )
    print(completion.choices[0].message.content)



if __name__ == "__main__":
    main()
