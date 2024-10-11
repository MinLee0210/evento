from typing import Optional

from components.base import BaseTool

class BaseAgent(BaseTool): 
    def __init__(self,
                api_key: Optional[str],
                model_name: Optional[str]
                ):

        self.api_key = api_key
        self.model_name = model_name


class LLMConfig:
    def __init__(self, 
                temperature: float = 0.8, 
                max_tokens: int = 512, 
                top_k:float=20, 
                top_p:float=0.8,):
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_k = top_k
        self.top_p = top_p

    def to_dict(self) -> dict:
        return {
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_k": self.top_k,
            "top_p": self.top_p,
        }