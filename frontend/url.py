# TODO: This should be in .env file

BACKEND_URL="http://localhost:8000"

# GET METHOD 
BACKEND_URL_GET_IMAGE=f"{BACKEND_URL}/search/image" # Add img_idx after the image: `/search/image/{image_idx}`
BACKEND_URL_GET_VIDEO_METADATA=f"{BACKEND_URL}/search/video" # Add vid_idx after the video: `/search/video/{vid_idx}`

# POST METHOD
BACKEND_URL_SEARCH_IMAGE=f"{BACKEND_URL}/search"
BACKEND_URL_SEARCH_OCR=f"{BACKEND_URL}/search/ocr"

