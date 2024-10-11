import os
import requests
from typing import Optional

try:
    from groq import Groq
except ImportError:
    raise ValueError(
        "Groq is not installed. Please install it with "
        "`pip install 'groq'`."
    )

from backend.app.components.llms.base import BaseAgent
from backend.app.components.llms.prompts import SYSTEM_PROMPT
class GroqAgent(BaseAgent):

    SUPPORTED_MODEL = {
        "llama3-8b": "llama3-8b-8192",
        "llama3-70b": "llama3-70b-8192",
        "mixtral-8x7b": "mixtral-8x7b-32768",
        "gemma-7b": "gemma-7b-it",
        }
    def __init__(self,
                api_key: Optional[str] = None,
                model_name: str='llama3-8b',
                max_retries:int=5,
                system_prompt:str=SYSTEM_PROMPT
                ):
                
        self.system_prompt=system_prompt
        api_key = api_key or os.getenv("GROQ_API_KEY")
                    
        if model_name not in self.SUPPORTED_MODEL:
            raise ValueError(f"Your input {model_name} is not supported. We support {', '.join(self.SUPPORTED_MODEL)}")

        super().__init__(api_key=api_key, model_name=model_name)
        
        self.model = Groq(api_key=api_key, max_retries=max_retries)

    def get_models(self):
        return ', '.join(self.SUPPORTED_MODEL)

    def run(self, input, text_only: bool = True,**kwargs):
        try:
            messages = [{"role": "user", "content": input}]
            if self.system_prompt:
                messages.backend.append(self.system_prompt)

            chat_completion = self.model.chat.completions.create(messages=messages, 
                                                                 model=self.model_name, 
                                                                 **kwargs)
            if text_only:
                return chat_completion.choices[0].message.content
            return chat_completion
        except ValueError as ve:
            raise ValueError("Got something wrong with the input") from ve
        except requests.exceptions.HTTPError as httpe:
            raise httpe