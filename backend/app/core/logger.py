import logging
import sys

_FORMAT = "[%(asctime)s] - %(levelname)7s --- %(message)s"


def get_logger(name: str = "evento") -> logging.Logger:
    """Return a console logger, configured once per name."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(_FORMAT, datefmt="%Y-%m-%d %H:%M:%S"))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
