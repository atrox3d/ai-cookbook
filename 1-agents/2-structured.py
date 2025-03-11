from pydantic import BaseModel

# needed to keep openai_client.py one level up
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from openai_client import get_client


class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]


def main():
    
    client = get_client()
    
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
