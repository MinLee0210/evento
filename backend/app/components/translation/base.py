from components.base import BaseTool

class BaseTranslation(BaseTool): 
    def __init__(self, from_lang=None, to_lang='en', auto_clean=False):
        self.from_lang = from_lang
        self.to_lang = to_lang
        self.auto_clean = auto_clean