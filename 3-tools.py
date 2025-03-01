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
    
    completion = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'system', 'content': 'you are a helpful assistant'},
            {'role': 'user', 'content': 'what is the weather like in Paris?'}
        ],
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


if __name__ == "__main__":
    main()
