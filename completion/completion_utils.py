import json
import requests

def call_external_api(messages, model, params):
    url = "https://api.opentyphoon.ai/v1/chat/completions"
    headers = {
        "Authorization": "Bearer sk-7rPYeT7qkoxvym07ebt9Kk8SVdz9rf5dv8jFM605Lqbf4aeh",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": messages,
        **params,
        "stream": True
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers, stream=True)

    if response.status_code != 200:
        raise ValueError(f"Error from API: {response.status_code} {response.text}")

    return response