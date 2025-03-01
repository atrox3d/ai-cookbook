import json
from openai_client import get_client
import requests

def get_weather(latitude, longitude):
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m"
        f"&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )
    data = response.json()
    return data['current'] #['temperature_2m']


def main():
    
    client = get_client()
    
    messages = [
            {'role': 'system', 'content': 'you are a helpful assistant'},
            {'role': 'user', 'content': 'what is the weather like in Paris?'}
        ]

    completion = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=messages,
        tools=[
            {
                'type': 'function',
                'function': {
                    'name': 'get_weather',
                    'description': 'Get the current weather for provided coordinates',
                    # parameters
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'latitude': {
                                'type': 'number',
                                'description': 'Latitude of the location'
                            },
                            'longitude': {
                                'type': 'number',
                                'description': 'Longitude of the location'
                            },
                        },
                        'required': ['latitude', 'longitude'],
                        'additionalProperties': False,
                    },  
                    # /parameters
                    'strict': True,
                }
            }
        ]
    )
    completion.model_dump()
    
    
    def call_function(name:str, args:dict):
        if name == 'get_weather':
            return get_weather(**args)
    
    
    for tool_call in completion.choices[0].message.tool_calls:
        message = completion.choices[0].message
        print(f'message: {message}')
        messages.append(message)
        
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        print(f'calling {name}({args})')
        result = call_function(name, args)
        print(f'result: {result}')
        
        tool_message = {
            'role': 'tool',
            'tool_call_id': tool_call.id,
            'content': str(result)
        }
        print(f'tool_message: {tool_message}')
        messages.append(tool_message)
        
        



if __name__ == "__main__":
    main()
