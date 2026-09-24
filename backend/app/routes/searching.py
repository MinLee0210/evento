from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import FileResponse

from schema.search import OcrSearchRequest, SearchResponse, TextSearchRequest
from services.keyframes import KeyframeNotFound
from services.search import SearchService

search_route = APIRouter(prefix="/search", tags=["search"])


def get_service(request: Request) -> SearchService:
    return request.app.state.search


@search_route.post("/", response_model=SearchResponse)
async def search(body: TextSearchRequest, service: SearchService = Depends(get_service)):
    try:
        return SearchResponse(hits=await run_in_threadpool(service.search, body))
    except KeyframeNotFound as e:
        raise HTTPException(404, f"Keyframe not found: {e}") from e


@search_route.post("/ocr", response_model=SearchResponse)
async def search_ocr(body: OcrSearchRequest, service: SearchService = Depends(get_service)):
    return SearchResponse(hits=await run_in_threadpool(service.search_ocr, body))


@search_route.get("/video/{video}")
async def get_video(video: str, service: SearchService = Depends(get_service)) -> dict:
    try:
        return service.catalog.video_metadata(video)
    except KeyframeNotFound as e:
        raise HTTPException(404, f"Video not found: {video}") from e


@search_route.get("/image/{image}")
async def get_image(image: str, service: SearchService = Depends(get_service)):
    try:
        path = service.catalog.image_path(image)
    except KeyframeNotFound as e:
        raise HTTPException(404, f"Image not found: {image}") from e
    return FileResponse(path, media_type=f"image/{Path(image).suffix.lstrip('.')}")
