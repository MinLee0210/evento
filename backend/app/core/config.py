import os
from dataclasses import dataclass

import torch

from components.translation import GoogleTranslator
from components.embedding.clip_ import ClipTool
from services.vector_store import VectorStore
from utils.helpers import ignore_warning

ignore_warning()

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
    vid_url = "vid_url.json"


@dataclass
class Config:
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    # device = 'cpu'
    environment = Environment()
    translator = GoogleTranslator()
    embedding_model = ClipTool(device=device)

    # TODO: Make this fix based on settings on this file, not in `setup_lifespan`
    vector_store = VectorStore
