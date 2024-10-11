from components.translation.base import BaseTranslation
from utils.pre_processing import clean

# import httpcore
# from typing import Any #type: ignore


# setattr(httpcore, 'SyncHTTPTransport', Any) #type: ignore


class GoogleTranslator(BaseTranslation):

    def __init__(self, from_lang=None, to_lang='en', auto_clean=False):
        super().__init__(from_lang=from_lang, to_lang=to_lang, auto_clean=auto_clean)
        if from_lang is None:
            self.from_lang = 'vi'
            
        try:
            import googletrans
            self.translator = googletrans.Translator()
        except ValueError as ve:
            raise ValueError('`googletrans` is not installed. Please try `pip install googletrans`') from ve
        
    def run(self, text: str) -> str:
        if self.auto_clean:
            text = clean(text)
        result = self.translator.translate(text).text
        return result
