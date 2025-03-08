import sys
import os
from pathlib import Path

# to use openai_client.py after moving tutorials under agents
# either :
#   - copy ../openai_client.py
#   * link to ../openai_client.py
#   - hack sys.argv
#   - use python -m agents.1-basic
#   
cwd = os.getcwd()       # ai-cookbook
cmdpath = Path(         # ai-cookbook/agents
    sys.argv[0]
).parent.absolute()
path = sys.path[0]      # ai-cookbook/agents


print(f'cwd     : {cwd}')
print(f'cmdpath : {cmdpath}')
print(f'path    : {path}')




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
    # main()
    ...
