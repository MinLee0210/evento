from components.base import BaseToolFactory

from ._blip import BlipTool
from ._clip import ClipTool


class EmbeddingFactory(BaseToolFactory):

    @staticmethod
    def produce(provider: str, **kwargs):
        try:
            match provider:
                case "blip":
                    return BlipTool(**kwargs)
                case "clip":
                    return ClipTool(**kwargs)
        except:
            raise ValueError(f"{provider} is not supported")
