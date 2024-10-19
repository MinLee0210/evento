import json
import os
import re 
from api.v1.searching import (
    get_video_metadata,
    # search_by_image_online,
    search_by_ocr,
    search_by_text,
    search_by_image
)
from api.v1.query_refine import refine_query
from core.config import Environment
from core.logger import set_logger
from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from utils.helpers import is_url

search_route = APIRouter(prefix="/search")

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
                # Normally, it executes 2 times and break.
                payload = json.loads(payload)
                print(type(payload))
                if type(payload) == dict:
                    break
                retries -= 1

        logging.info("search_text: get data from request ...")
        query = payload.get("query")
        top_k = payload.get("top_k", 20)  # Default to 20 if not provided
        high_performance = payload.get("high_performance", "clip")
        smart_query = payload.get('smart_query')
        print(high_performance)

        if not query:
            raise HTTPException(status_code=400, detail="Missing query parameter")

        # Validate top_k
        if not isinstance(top_k, int) or top_k <= 0:
            raise HTTPException(
                status_code=400,
                detail="Invalid top_k value. Must be a positive integer.",
            )

        vector_store = request.app.state.vector_store[high_performance]
        if is_url(query):
            logging.info("query is an URL")
            results = search_by_image(
                image_path=query,
                top_k=top_k,
                vector_store=vector_store,
                vid_url=request.app.state.vid_url,
                url_fps=request.app.state.url_fps,
                online=True
            )
        elif re.match(r'^L\d{2}_V\d{3},\s*(\d|[1-9]\d{0,4})$', query):
            logging.info("query is an video id")
            keyframes = request.app.state.keyframes

            input_vid_name, input_frame = query.split(', ')
             
            input_frame = int(input_frame)
            filtered_df = keyframes[(keyframes['vid_name'] == input_vid_name) & (keyframes['shot'].apply(lambda x: eval(x)[0] <= input_frame <= eval(x)[1]))]

            closest_row = filtered_df.iloc[(filtered_df['frame'] - input_frame).abs().argsort()[:1]]
            text_query = f"{closest_row['vid_name'].values[0]}, {str(closest_row['frame'].values[0]).zfill(5)}"
            logging.info("1")

            image_path = os.path.join(request.app.state.env_dir.root, request.app.state.env_dir.db_root, request.app.state.env_dir.lst_keyframes['path'] , '-'.join(text_query.split(', ')) + '.webp')
            logging.info(image_path)
            results = search_by_image(
                img_path=image_path,
                top_k=top_k,
                vector_store=vector_store,
                vid_url=request.app.state.vid_url,
                url_fps=request.app.state.url_fps,
                online=False
            )
        else: 
            logging.info("query is a text")
            translator = request.app.state.translator
            logging.info("search_text: start querying ...")
            translated_query = translator.run(query)
            try: 
                logging.info('enter smart_query')
                if smart_query: 
                    translated_query = refine_query(translated_query)['refine_response']
            except:
                logging.info('running smart_query fail')
            logging.debug(translated_query)

            results = search_by_text(
                translated_query,
                top_k,
                vector_store,
                request.app.state.vid_url,
                request.app.state.url_fps,
            )

        #  Crucially, check the structure of your results
        if not isinstance(results, dict) or not all(
            k in results
            for k in ["scores", "idx_image", "infos_query", "vid_urls", "frames"]
        ):
            raise HTTPException(
                status_code=500,
                detail="Invalid response format from search_images function.",
            )

        if not isinstance(results["scores"][0], list):
            raise HTTPException(status_code=500, detail="Invalid scores format.")

        # Ensure the lengths are consistent as expected by the frontend.
        if (
            len(results["idx_image"]) != len(results["scores"][0])
            or len(results["infos_query"]) != len(results["scores"][0])
            or len(results["vid_urls"]) != len(results["scores"][0])
            or len(results["frames"]) != len(results["scores"][0])
        ):
            raise HTTPException(
                status_code=500, detail="Inconsistent array lengths in results."
            )

        return JSONResponse(jsonable_encoder(results))

    except Exception as e:
        # Better error handling, log error and return specific error message
        print(f"An error occurred: {e}")  # Log the exception for debugging
        return JSONResponse({"error": str(e)}, status_code=500)

@search_route.post("/ocr")
async def search_with_ocr_matching(request: Request):
    retries = 3
    try:
        logging.info("Invoke search_with_ocr_matching ...")
        payload = await request.json()

        if isinstance(payload, str):
            logging.info("search_with_ocr_matching: converting string to json")
            while retries >= 0:
                # Normally, it executes 2 times and break.
                payload = json.loads(payload)
                print(type(payload))
                if type(payload) == dict:
                    break
                retries -= 1

        logging.info("search_with_ocr_matching: get data from request ...")
        query = payload.get("query")
        top_k = payload.get("top_k", 20)  # Default to 20 if not provided
        mode = payload.get("mode", 0)
        if not query:
            raise HTTPException(status_code=400, detail="Missing query parameter")

        # Validate top_k
        if not isinstance(top_k, int) or top_k <= 0:
            raise HTTPException(
                status_code=400,
                detail="Invalid top_k value. Must be a positive integer.",
            )

        logging.info("search_with_ocr_matching: start searching ...")

        results = search_by_ocr(
            query=query,
            top_k=top_k,
            matching_tool=request.app.state.matching_tool,
            mode=mode,
            llm=None,
            vid_url=request.app.state.vid_url,
            url_fps=request.app.state.url_fps,
        )

        # results = search_by_ocr(
        #     query=query,
        #     top_k=top_k,
        #     matching_tool=request.app.state.matching_tool,
        #     mode=mode,
        #     llm=request.app.state.kw_llm_agent,
        #     vid_url=request.app.state.vid_url,
        #     url_fps=request.app.state.url_fps,
        # )

        return JSONResponse(jsonable_encoder(results))

    except Exception as e:
        # Better error handling, log error and return specific error message
        print(f"An error occurred: {e}")  # Log the exception for debugging
        return JSONResponse({"error": str(e)}, status_code=500)


@search_route.get("/video/{vid_idx}")
async def get_video(vid_idx: str):
    try:

        logging.info("Invoke get_video ...")

        vid_name = ".".join([vid_idx, "json"])
        video_metadata = get_video_metadata(
            vid_idx=vid_name,
            media_dir=os.path.join(env_dir.root, env_dir.db_root, env_dir.media_info),
        )
        logging.info("get_video: sending the image ...")
        return JSONResponse(content=jsonable_encoder(video_metadata), status_code=200)

    except HTTPException as httpe:
        raise HTTPException(
            status_code=404, detail="Get something wrong from the function"
        ) from httpe


@search_route.get("/image/{image_idx}")
async def get_image(image_idx: str):
    # Search image based on image_idx.
    # TODO: Add exception
    try:

        logging.info("Invoke get_image ...")

        image_type = image_idx.split(".")[-1]
        image_path = os.path.join(
            env_dir.root, env_dir.db_root, env_dir.lst_keyframes["path"], image_idx
        )
        logging.info(image_path)

        logging.info("get_image: sending the image ...")
        with open(image_path, "rb") as f:
            return Response(
                content=f.read(), media_type=f"image/{image_type}", status_code=200
            )

    except HTTPException as httpe:
        raise HTTPException(
            status_code=404, detail="Get something wrong from the function"
        ) from httpe
