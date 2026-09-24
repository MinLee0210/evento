import json
from typing import Literal

from pydantic import BaseModel, Field, PositiveInt, field_validator, model_validator

from components.query_refiner import RefineMode

EmbedderName = Literal["clip", "blip", "blip_des", "blip_fct"]


class _Request(BaseModel):
    query: str = Field(min_length=1)
    top_k: PositiveInt = 20

    @model_validator(mode="before")
    @classmethod
    def _decode_json_string(cls, data):
        # Older clients post `json.dumps(payload)`, i.e. a JSON-encoded string.
        return json.loads(data) if isinstance(data, str) else data


class TextSearchRequest(_Request):
    high_performance: EmbedderName = "clip"
    smart_query: RefineMode = "plain"

    @field_validator("high_performance", "smart_query", mode="before")
    @classmethod
    def _lower(cls, value):
        return value.lower() if isinstance(value, str) else value


class OcrSearchRequest(_Request):
    mode: int = Field(0, ge=0, lt=8)


class Hit(BaseModel):
    image: str = Field(description="Keyframe file name, e.g. `L01_V001-00123.webp`")
    video: str
    frame: int
    url: str = Field(description="Video URL seeked to this keyframe")
    score: float


class SearchResponse(BaseModel):
    hits: list[Hit]
