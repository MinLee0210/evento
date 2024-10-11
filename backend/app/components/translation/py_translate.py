from components.translation.base import BaseTranslation
from utils.pre_processing import clean

class PyTranslator(BaseTranslation):

    def __init__(self, from_lang='vi', to_lang='en', auto_clean=False):
        super().__init__(from_lang=from_lang, to_lang=to_lang, auto_clean=auto_clean)

        if from_lang is None:
            self.from_lang = 'autodetect'
        try:
            import translate
            self.translator = translate.Translator(from_lang=self.from_lang, to_lang=self.to_lang)
        except ValueError:
            raise ValueError('`translate` is not installed. Please try `pip install translate`')
    
    def run(self, text: str) -> str:
        if self.auto_clean:
            text = clean(text)
        result = self.translator.translate(text)
        return result