import requests


def get_quote(url: str):
    try:
        if not url:
            raise ValueError("URL is missing")
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


def setup_url(url: str = "http://103.20.97.119:8080"):
    BACKEND_URL = url

    # GET METHOD
    BACKEND_URL_GET_IMAGE = f"{BACKEND_URL}/search/image"  # Add img_idx after the image: `/search/image/{image_idx}`
    BACKEND_URL_GET_VIDEO_METADATA = f"{BACKEND_URL}/search/video"  # Add vid_idx after the video: `/search/video/{vid_idx}`

    # POST METHOD
    BACKEND_URL_SEARCH_IMAGE = f"{BACKEND_URL}/search"
    BACKEND_URL_SEARCH_OCR = f"{BACKEND_URL}/search/ocr"

    return (
        BACKEND_URL,
        BACKEND_URL_GET_IMAGE,
        BACKEND_URL_GET_VIDEO_METADATA,
        BACKEND_URL_SEARCH_IMAGE,
        BACKEND_URL_SEARCH_OCR,
    )
