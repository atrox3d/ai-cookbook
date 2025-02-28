import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel


class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]


def main():
    load_dotenv()
    assert os.getenv("OPENAI_API_KEY") is not None, "OPENAI_API_KEY is not set"
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    completion = client.beta.chat.completions.parse(
        model='gpt-4o-mini',
        messages=[
            {'role': 'system', 'content': 'Extract the event information'},
            {'role': 'user', 'content': 'Alice and Bob are going to a science fair on Friday'}
        ],
        response_format=CalendarEvent
    )
    print(completion.choices[0].message.parsed)
    print(completion.choices[0].message.parsed.model_dump())



if __name__ == "__main__":
    main()
