
from components.base import BaseToolFactory
from ._fuzzywuzzy import FuzzyMatchingTool
from ._rapidwuzzy import RapidMatchingTool

# TODO: Refactor the FuzzyMatching so that it only read from config, not implement config.
class FuzzyMatchingFactory(BaseToolFactory): 

    @staticmethod
    def produce(provider:str='rapidwuzzy', **kwargs): 
        try: 
            match provider: 
                case 'fuzzywuzzy': 
                    return FuzzyMatchingTool(**kwargs)
                case 'rapidwuzzy': 
                    return RapidMatchingTool(**kwargs)
        except: 
            raise ValueError(f"{provider} is not supported")

