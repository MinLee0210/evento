"Setup logger for keeping track while the system is running."

import os
import logging
from datetime import datetime

class DualHandler(logging.Handler):
    "Builing Configuration for logger"
    def __init__(self, filename=None, level=logging.NOTSET):
        logging.Handler.__init__(self, level)
        self.console_handler = logging.StreamHandler()
        self.file_handler = logging.FileHandler(filename, mode='a')
        self.formatter = logging.Formatter('[%(asctime)s] - %(levelname)7s --- %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        self.console_handler.setFormatter(self.formatter)
        self.file_handler.setFormatter(self.formatter)

    def emit(self, record):
        self.console_handler.emit(record)
        self.file_handler.emit(record)

def set_logger(level:int=logging.DEBUG, file_dir='./log') -> logging.Logger:
    "Setup Logger"
    logger = logging.getLogger(__name__)
    logger.handlers.clear() # Clear duplicate events
    logger.setLevel(level)

    if os.path.exists(file_dir): 
        to_day = str(datetime.now().strftime('%Y-%m-%d::%H:%M:%S'))
        file_path = os.path.join(file_dir, f"app_{to_day}.log")
    else: 
        file_path = 'app.log'
        
    dual_handler = DualHandler(file_path)
    logger.addHandler(dual_handler)

    return logger