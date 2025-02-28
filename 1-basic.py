from openai_client import get_client


def main():
    
    client = get_client()
    
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
