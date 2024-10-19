import os
from dataclasses import dataclass

import torch
from components.embedding import EmbeddingFactory
from components.fuzzymatching._rapidwuzzy import RapidMatchingTool
from components.llms import AgentFactory
from components.translation import GoogleTranslator
from dotenv import load_dotenv
from schema.llm_response import Keyword
from services.vector_store import VectorStore
from utils.helpers import ignore_warning

ignore_warning()
load_dotenv()


@dataclass
class Environment:
    # root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    # Database path
    db_root = "db"  # Need to go outside `/backend`
    features = "features"
    media_info = "media-info"
    lst_keyframes = {"path": "s_optimized_keyframes", "format": ".webp"}
    keyframes = "keyframes.csv"
    vid_url = "vid_url.json"
    url_fps = "url_fps.json"


@dataclass
class Config:

    device = "cuda" if torch.cuda.is_available() else "cpu"

    # TODO: Re-construct this part
    EMBEDDING_CONFIG = {"device": device}
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    KW_LLM_CONFIG = {
        "api_key": GOOGLE_API_KEY,
        "response_setting": {
            "response_mime_type": "application/json",
            "response_schema": list[Keyword],
        },
    }
    MATCHING_TOOL_CONFIG = {"csv_path": "./db/keyframes.csv", "env_dir": Environment()}

    environment = Environment()
    translator = GoogleTranslator()
    embedding_model_clip = EmbeddingFactory.produce(provider="clip", **EMBEDDING_CONFIG)
    embedding_model_blip = EmbeddingFactory.produce(provider="blip", **EMBEDDING_CONFIG)

    EMBEDDING_CONFIG_BLIP_DES = {"device": device, 
                                 "model_id": "blip2_des"}
    embedding_model_blip_des = EmbeddingFactory.produce(provider="blip", **EMBEDDING_CONFIG_BLIP_DES)

    EMBEDDING_CONFIG_BLIP_FCT = {"device": device,
                                 "model_id": "blip2_fct"}
    embedding_model_blip_fct = EmbeddingFactory.produce(provider="blip", **EMBEDDING_CONFIG_BLIP_FCT)


    vector_store = VectorStore

    kw_llm_agent = AgentFactory.produce(provider="gemini", **KW_LLM_CONFIG)

    ocr_matcher = RapidMatchingTool(**MATCHING_TOOL_CONFIG)
