import os
import json
import glob
from contextlib import asynccontextmanager

from core.config import Config
from core.logger import set_logger
from utils.helpers import ignore_warning, get_to_root

get_to_root()
ignore_warning()

config = Config()
logging = set_logger()

@asynccontextmanager
async def lifespan(app): 
    """
    Sets up and cleans up application resources during the FastAPI lifespan.

    This function is executed during the application startup and shutdown phases.
    It initializes key components like paths, translator, embedding model,
    and vector store, and cleans them up during shutdown.


    Args:
        app (FastAPI): The FastAPI application instance.
        
    """
    logging.info("Setup lifespan ...")

    logging.info("Setup Paths ...")
    env_dir = config.environment
    lst_keyframes = glob.glob(os.path.join(env_dir.root,
                                           env_dir.db_root, 
                                           f"{env_dir.lst_keyframes['path']}", 
                                           f"*{env_dir.lst_keyframes['format']}"))
    lst_keyframes.sort()

    id2img_fps = dict()
    for i, img_path in enumerate(lst_keyframes):
        id2img_fps[i] = img_path

    with open(os.path.join(env_dir.root, env_dir.db_root, env_dir.vid_url), 'r') as f:
        app.state.vid_url = json.load(f)
        
    with open(os.path.join(env_dir.root, env_dir.db_root, env_dir.url_fps), 'r') as f:
        app.state.url_fps = json.load(f)
        
    # Setup Translator
    logging.info("Setup Translator ...")
    app.state.translator = config.translator
    
    
    # Setup Embedding Model
    logging.info("Setup Embedding Model ...")
    # app.state.embedding_model_blip = config.embedding_model_blip
    app.state.embedding_model_clip = config.embedding_model_clip


    # Setup Vector Store
    logging.info("Setup Vector Store ...")
    db_features = os.path.join(env_dir.db_root, env_dir.features)
    # project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    bin_file= os.path.join(env_dir.root, db_features, f'{config.embedding_model_clip.bin_name}.bin')
    vector_store_clip = config.vector_store(env_dir.root, bin_file, id2img_fps, config.device, config.embedding_model_clip)
    # vector_store_blip = config.vector_store(env_dir.root, bin_file, id2img_fps, config.device, config.embedding_model_blip)
    app.state.vector_store_clip = vector_store_clip
    # app.state.vector_store_blip = vector_store_blip

    yield
    
    logging.info("Clean up lifespan ...")

    del app.state.translator
    del app.state.embedding_model_clip
    del app.state.vector_store_clip    

    logging.info("DONE!!!")

