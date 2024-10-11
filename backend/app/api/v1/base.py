"""
When the frontend triggers its first requests to backend, it should trigger this route to test the connection between frontend and backend.
"""

import requests
from json import loads


def generate_quote(url="https://zenquotes.io/api/random"):
    response = requests.get(url)
    json_data = loads(response.text)
    quote = (
        f'''"{json_data[0]["q"]}" - {json_data[0]['a']}'''
    ) 
    # '"' + json_data[0]["q"] + '"' + " - " + json_data[0]["a"]
    return quote