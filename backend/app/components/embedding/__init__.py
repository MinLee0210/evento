
from components.base import BaseToolFactory
from .blip_ import BlipTool
from .clip_ import ClipTool

class EmbeddingFactory(BaseToolFactory): 

    @staticmethod
    def produce(provider, **kwargs): 
        try: 
            match provider: 
                case 'blip': 
                    return BlipTool(**kwargs)
                case 'clip': 
                    return ClipTool(**kwargs)
        except: 
            raise ValueError(f"{provider} is not supported")

