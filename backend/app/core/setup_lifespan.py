import glob
import json
import os
from contextlib import asynccontextmanager

import pandas as pd

from core.config import Config
from core.logger import set_logger
from utils.helpers import get_to_root, ignore_warning

get_to_root()
ignore_warning()

config = Config()
logging = set_logger()


@asynccontextmanager
async def lifespan(app):
    """
    Sets up and cleans up application resources during the FastAPI lifespan.
    """
    logging.info("Setup lifespan ...")

    logging.info("Setup Paths ...")
    env_dir = config.environment
    lst_keyframes = glob.glob(
        os.path.join(
            env_dir.root,
            env_dir.db_root,
            f"{env_dir.lst_keyframes['path']}",
            f"*{env_dir.lst_keyframes['format']}",
        )
    )
    lst_keyframes.sort()

    id2img_fps = dict()
    for i, img_path in enumerate(lst_keyframes):
        id2img_fps[i] = img_path

    with open(os.path.join(env_dir.root, env_dir.db_root, env_dir.vid_url), "r") as f:
        app.state.vid_url = json.load(f)

    with open(os.path.join(env_dir.root, env_dir.db_root, env_dir.url_fps), "r") as f:
        app.state.url_fps = json.load(f)

    app.state.keyframes = pd.read_csv(os.path.join(env_dir.root, env_dir.db_root, env_dir.keyframes), sep="|")
    
    # Setup Translator
    logging.info("Setup Translator ...")
    app.state.translator = config.translator

    # Setup Embedding Model
    logging.info("Setup Embedding Model ...")
    app.state.embedding_model = {
        "clip": config.embedding_model_clip,
        "blip": config.embedding_model_blip,
        "blip_des": config.embedding_model_blip_des,
        "blip_fct": config.embedding_model_blip_fct,
    }

    # Setup LLM agent
    app.state.kw_llm_agent = config.kw_llm_agent

    # Setup matching tool
    app.state.matching_tool = config.ocr_matcher

    # Setup Vector Store
    logging.info("Setup Vector Store ...")
    db_features = os.path.join(env_dir.db_root, env_dir.features)
    bin_file = {
        "clip": os.path.join(
            env_dir.root, db_features, f"{config.embedding_model_clip.bin_name}.bin"
        ),
        "blip": os.path.join(
            env_dir.root, db_features, f"{config.embedding_model_blip.bin_name}.bin"
        ),
        "blip_des": os.path.join(
            env_dir.root, db_features, f"{config.embedding_model_blip.bin_name}.bin"
        ),
        "blip_fct": os.path.join(
            env_dir.root, db_features, f"{config.embedding_model_blip.bin_name}.bin"
        ),
    }

    app.state.vector_store = {
        "clip": config.vector_store(
            env_dir.root,
            bin_file["clip"],
            id2img_fps,
            config.device,
            config.embedding_model_clip,
        ),
        "blip": config.vector_store(
            env_dir.root,
            bin_file["blip"],
            id2img_fps,
            config.device,
            config.embedding_model_blip,
        ),
        "blip_des": config.vector_store(
        env_dir.root,
        bin_file["blip"],
        id2img_fps,
        config.device,
        config.embedding_model_blip_des,
        ),
        "blip_fct": config.vector_store(
        env_dir.root,
        bin_file["blip"],
        id2img_fps,
        config.device,
        config.embedding_model_blip_fct,
        ),
    }

    yield

    logging.info("Clean up lifespan ...")

    del app.state.translator
    del app.state.matching_tool
    del app.state.kw_llm_agent
    del app.state.embedding_model
    del app.state.vector_store

    logging.info("DONE!!!")
