import os 
import json

from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.responses import JSONResponse

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
    try: 

        logging.info("Invoke search_text ...")
        payload = await request.json()
        payload = json.loads(payload)

        logging.info("search_text: get data from request ...")
        query, top_k = payload['query'], payload['top_k']
        translator = request.app.state.translator
        vector_store = request.app.state.vector_store

        logging.info("search_text: start querying ...")
        translated_query = translator.run(query)
        logging.debug(translated_query)
        results = search_by_text(translated_query, top_k, vector_store)

        return JSONResponse(content=results, 
                        media_type="application/json", 
                        status_code=200)
    
    except HTTPException as httpe: 
        raise HTTPException(status_code=404, 
                            detail="Get something wrong from the function") from httpe

@search_route.get('/{image_idx}')
async def get_image(image_idx: str): 
    # Search image based on image_idx.
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