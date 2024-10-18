from pydantic import BaseModel, Field
from typing import Any

class BaseReponse(BaseModel): 
    image_paths: list[str] = Field(..., description="List of image paths")
    vid_urls: list[str] = Field(..., description="List of video's url at the exact time `t`")
    frames: list[Any] = Field(..., description="List of frames index")


class SearchResponse(BaseReponse):
    scores: list[float] = Field(...,description="")
    infos_query: list[str] = Field(..., description="")
    idx_image: list[str] = Field(..., description="")
