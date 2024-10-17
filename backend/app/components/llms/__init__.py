from components.base import BaseToolFactory

from .gemini import GeminiAgent
# from .groq import GroqAgent

class AgentFactory(BaseToolFactory): 
    
    @staticmethod
    def produce(provider: str, **kwargs):
        try: 
            match provider: 
                case 'gemini': 
                    return GeminiAgent(**kwargs)
                # case 'groq': 
                #     return GroqAgent(**kwargs)
        except Exception as e: 
            raise ValueError(f'Some errors occured: {e}')