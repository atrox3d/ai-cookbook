import json

from pydantic import BaseModel, Field
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

    tools = [
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

    completion = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=messages,
        tools=tools
    )
    completion.model_dump()
    
    
    def call_function(name:str, args:dict):
        if name == 'get_weather':
            return get_weather(**args)
    
    
    for tool_call in completion.choices[0].message.tool_calls:
        message = completion.choices[0].message
        print(f'message: {message}')
        messages.append(message.model_dump())
        
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
        
    
    class WeatherResponse(BaseModel):
        temperature: float = Field(
            description='the current temperature for the given coordinates'
        )
        response: str = Field(
            description='a natural language response to the user\'s question'
        )
    print()
    [print(_message) for _message in messages]
    final_completion = client.beta.chat.completions.parse(
        model='gpt-4o-mini',
        messages=messages,
        tools=tools,
        response_format=WeatherResponse
    )
    final_response = final_completion.choices[0].message.parsed
    print(f'final_response: {final_response}')
    
    

if __name__ == "__main__":
    main()
