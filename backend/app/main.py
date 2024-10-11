import uvicorn
from core.setup_lifespan import lifespan
from core.setup_app import setup_app
from utils.helpers import ignore_warning, get_to_root

get_to_root()
ignore_warning()
import subprocess; print(subprocess.run(['pwd']))
app = setup_app(lifespan)


# if __name__ == "__main__": 
#     uvicorn.run("main:app", 
#                 host="0.0.0.0",  
#                 port=8000, 
#                 log_level="info", 
#                 reload=True
#                 )