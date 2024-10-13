import json
import requests
from PIL import Image

import streamlit as st


@st.cache_data
def search_image_by_text(url:str, data:dict): 
    try: 
        if not url: 
           raise ValueError("URL is missing")
        
        # TODO: Check data format, include: `query`, `top_k`, `strength`
        # Send the POST request
        response = requests.post(url, 
                                json=json.dumps(data))

        # Check for successful response
        if response.status_code == 200:  # 201 Created
            print("Post created successfully!")
            return response.json()
        else:
            print(f"Error creating post: {response.status_code}")
            raise requests.HTTPError(f"Error {response.status_code}: {response.text}")
    except Exception as e: 
        raise requests.HTTPError(e)
    

def get_image(url, image_idx): 
    get_image_url = f"{url}/{image_idx}"
    img = Image.open(requests.get(get_image_url, stream=True).raw).convert('RGB')
    return img