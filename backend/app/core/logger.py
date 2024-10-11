import logging

class DualHandler(logging.Handler):
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

def set_logger(level:int=logging.DEBUG, file_path:str='app.log') -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.handlers.clear() # Clear existing handlers
    logger.setLevel(level)

    dual_handler = DualHandler(file_path)
    logger.addHandler(dual_handler)

    return logger