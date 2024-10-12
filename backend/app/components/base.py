from abc import ABC, abstractmethod
from typing import Any

class BaseTool(ABC):

    @abstractmethod
    def run(self, input:Any) -> Any: 
        raise NotImplementedError
    

class BaseToolFactory(ABC): 

    @staticmethod
    def produce(provider:str, **kwargs): 
        raise NotImplementedError