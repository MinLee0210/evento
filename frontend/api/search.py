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
            # print("Post created successfully!")
            return response.json()
        else:
            # print(f"Error creating post: {response.status_code}")
            raise requests.HTTPError(f"Error {response.status_code}: {response.text}")
    except Exception as e: 
        raise requests.HTTPError(e)

def get_image(url, image_idx): 
    try: 
        get_image_url = f"{url}/{image_idx}"
        response = requests.get(get_image_url, stream=True)
        if response.status_code == 200:  # 201 Created
            # print("Get created successfully!")
            img = Image.open(response.raw).convert('RGB')
            return img
        else:
            # print(f"Error creating get: {response.status_code}")
            raise requests.HTTPError(f"Error {response.status_code}: {response.text}")

    except Exception as e: 
        raise requests.HTTPError(e)

def get_video_metadata(url, vid_idx): 
    try: 
        get_vid_metadata_url = f"{url}/{vid_idx}"
        response = requests.get(get_vid_metadata_url)
                # Check for successful response
        if response.status_code == 200:  # 201 Created
            # print("Get created successfully!")
            return response.json()
        else:
            # print(f"Error creating get: {response.status_code}")
            raise requests.HTTPError(f"Error {response.status_code}: {response.text}")
    except Exception as e: 
        raise requests.HTTPError(e)