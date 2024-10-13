import os 
import json

from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from api.v1.searching import search_by_text

from core.config import Environment
from core.logger import set_logger

search_route = APIRouter(
    prefix="/search"
)

env_dir = Environment()
logging = set_logger()

@search_route.post("/")
async def search_text(request: Request): 
    # Search related images based on text-based query.
    retries = 3

    try: 

        logging.info("Invoke search_text ...")
        payload = await request.json()
        
        if isinstance(payload, str): 
            logging.info("search_text: converting string to json")
            while retries >= 0: 
                payload = json.loads(payload)
                print(type(payload))
                if type(payload) == dict: 
                    break
                
                retries -= 1

        logging.info("search_text: get data from request ...")
        query = payload.get("query")
        top_k = payload.get("top_k", 20)  # Default to 20 if not provided

        if not query:
            raise HTTPException(status_code=400, detail="Missing query parameter")


        # Validate top_k
        if not isinstance(top_k, int) or top_k <= 0:
          raise HTTPException(status_code=400, detail="Invalid top_k value. Must be a positive integer.")
        
        translator = request.app.state.translator
        vector_store = request.app.state.vector_store_clip

        logging.info("search_text: start querying ...")
        translated_query = translator.run(query)
        logging.debug(translated_query)

        results = search_by_text(translated_query, top_k, vector_store, request.app.state.vid_url, request.app.state.url_fps)
        
        #  Crucially, check the structure of your results
        if not isinstance(results, dict) or not all(k in results for k in ["scores", "idx_image", "infos_query", "vid_urls", "frames"]):
           raise HTTPException(status_code=500, detail="Invalid response format from search_images function.")
        
        if not isinstance(results["scores"][0], list):
           raise HTTPException(status_code=500, detail="Invalid scores format.")
          
        # Ensure the lengths are consistent as expected by the frontend.
        if len(results["idx_image"]) != len(results["scores"][0]) or \
            len(results["infos_query"]) != len(results["scores"][0]) or \
            len(results['vid_urls']) != len(results["scores"][0]) or \
            len(results['frames']) != len(results['scores'][0]):
          raise HTTPException(status_code=500, detail="Inconsistent array lengths in results.")
        
        return JSONResponse(jsonable_encoder(results))
    
    except Exception as e:
        # Better error handling, log error and return specific error message
        print(f"An error occurred: {e}")  # Log the exception for debugging
        return JSONResponse({"error": str(e)}, status_code=500)

@search_route.get('/image/{image_idx}')
async def get_image(image_idx: str): 
    # Search image based on image_idx.
    # TODO: Add exception
    try:

        logging.info("Invoke get_image ...")

        image_type = image_idx.split('.')[-1]
        image_path = os.path.join(env_dir.root, 
                                  env_dir.db_root, 
                                  env_dir.lst_keyframes['path'], 
                                  image_idx)
        logging.info(image_path)

        logging.info("get_image: sending the image ...")
        with open(image_path, "rb") as f:
            return Response(content=f.read(), 
                            media_type=f"image/{image_type}",
                            status_code=200)
        
    except HTTPException as httpe: 
        raise HTTPException(status_code=404, 
                            detail="Get something wrong from the function") from httpe