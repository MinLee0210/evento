import os
from dataclasses import dataclass
from dotenv import load_dotenv

import torch

from components.translation import GoogleTranslator
from components.llms import AgentFactory
from components.fuzzymatching import FuzzyMatchingFactory

from components.embedding.clip_ import ClipTool
# from components.embedding.blip_ import BlipTool
from services.vector_store import VectorStore
from utils.helpers import ignore_warning

ignore_warning()
load_dotenv()
@dataclass
class Environment:
    # root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    # Database path
    db_root = "db"                  # Need to go outside `/backend`
    features = "features"
    lst_keyframes = {
        'path': "s_optimized_keyframes", 
        "format": ".webp"
    }
    keyframes = 'keyframes.csv'
    vid_url = "vid_url.json"
    url_fps = "url_fps.json"

@dataclass
class Config:
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    # device = 'cpu'
    environment = Environment()
    translator = GoogleTranslator()
    embedding_model_clip = ClipTool(device=device)
    # embedding_model_blip = BlipTool(device=device)

    # TODO: Make this fix based on settings on this file, not in `setup_lifespan`
    vector_store = VectorStore

    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    llm_config = {'api_key': GOOGLE_API_KEY}
    llm_agent = AgentFactory.produce(provider='gemini', 
                                    **llm_config)

    matching_tool_config = {'csv_path': './backend/db/keyframes.csv', 
                            'env_dir': Environment()}
    ocr_matcher = FuzzyMatchingFactory.produce('rapidwuzzy', **matching_tool_config)