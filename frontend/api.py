import json
import requests

import streamlit as st

from .url import (BACKEND_URL, 
                  BACKEND_URL_GET_IMAGE,                    # GET
                  BACKEND_URL_SEARCH_IMAGE)                 # POST


def get_quote(url:str):
    try: 
        if not url: 
            url = BACKEND_URL
        quote_res = requests.get(url)
        # Check for successful response
        if quote_res.status_code == 200:  # 201 Created
            print("GET created successfully!")
            return quote_res.json()
        else:
            print(f"Error creating GET: {quote_res.status_code}")
            raise requests.HTTPError(f"Error {quote_res.status_code}: {quote_res.text}")
    except Exception as e: 
        raise requests.HTTPError(e)

@st.cache_data
def search_image_by_text(url:str, data:dict): 
    try: 
        if not url: 
            url = BACKEND_URL_GET_IMAGE

        # TODO: Check data format, include: `query`, `top_k`, `strength`
        # Send the POST request
        response = requests.post(url, 
                                json=json.dumps(data))

        # Check for successful response
        if response.status_code == 201:  # 201 Created
            print("Post created successfully!")
            return response.json()
        else:
            print(f"Error creating post: {response.status_code}")
            raise requests.HTTPError(f"Error {response.status_code}: {response.text}")
    except Exception as e: 
        raise requests.HTTPError(e)