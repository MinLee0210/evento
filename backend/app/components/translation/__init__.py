
# from models.translation.pretrained_models import M2M100Translator, MarianTranslator, PretrainedModelTranslator, EnvT5Translator

from components.base import BaseToolFactory
from .google_translate import GoogleTranslator
from .py_translate import PyTranslator


class TranslatorFactory(BaseToolFactory): 
    @staticmethod
    def produce(provider, **kwargs): 
        try: 
            match provider: 
                case 'googletrans': 
                    return GoogleTranslator(**kwargs)
                case 'py_translate': 
                    return PyTranslator(**kwargs)
        except: 
            raise ValueError(f"{provider} is not supported")