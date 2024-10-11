from typing import Any

from components.translation.base import BaseTranslation
from utils.pre_processing import clean

# HuggingFace's model card: Helsinki-NLP/opus-mt-vi-en
class MarianTranslator(BaseTranslation):
    def __init__(self, from_lang=None, to_lang='en', auto_clean=False):
        super().__init__(from_lang=from_lang, to_lang=to_lang, auto_clean=auto_clean)
        self.model_id = "Helsinki-NLP/opus-mt-vi-en"

        try:
            from transformers import MarianMTModel, MarianTokenizer
            self.tokenizer = MarianTokenizer.from_pretrained(self.model_id)
            self.model = MarianMTModel.from_pretrained(self.model_id).eval()
        except:
            raise ValueError(f'Error loading model {self.model_id}. `transformers` is not installed. Please try `pip install transformers`')
        
    def run(self, text) -> str:
        if self.auto_clean: 
            text = clean(text)
        input_ids = self.tokenizer(text, return_tensors="pt").input_ids
        outputs = self.model.generate(input_ids)
        result = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return result
    

# HuggingFace's model card: Helsinki-NLP/opus-mt-vi-en
class M2M100Translator(BaseTranslation):
    def __init__(self, from_lang=None, to_lang='en', auto_clean=False):
        super().__init__(from_lang=from_lang, to_lang=to_lang, auto_clean=auto_clean)
        self.model_id = "facebook/m2m100_418M"
        try:
            from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
            self.tokenizer = M2M100Tokenizer.from_pretrained(self.model_id)
            self.model = M2M100ForConditionalGeneration.from_pretrained(self.model_id).eval()
        except:
            raise ValueError(f'Error loading model {self.model_id}. `transformers` is not installed. Please try `pip install transformers`')

    def run(self, text) -> str:
        if self.auto_clean: 
            text = clean(text)
        self.tokenizer.src_lang = "vi"
        input_ids = self.tokenizer(text, return_tensors="pt").input_ids
        outputs = self.model.generate(input_ids, forced_bos_token_id=self.tokenizer.get_lang_id("en"))
        result = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return result


# HuggingFace's model card: VietAI/envit5-translation
class EnvT5Translator(BaseTranslation):
    def __init__(self, from_lang=None, to_lang='en', auto_clean=False):
        super().__init__(from_lang=from_lang, to_lang=to_lang, auto_clean=auto_clean)
        self.model_id = "VietAI/envit5-translation"
        try:
            from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_id).eval()
        except:
            raise ValueError(f'Error loading model {self.model_id}. `transformers` is not installed. Please try `pip install transformers`')

    def run(self, text) -> str:
        if self.auto_clean: 
            text = clean(text)
        input_ids = self.tokenizer(text, return_tensors="pt").input_ids
        outputs = self.model.generate(input_ids)
        result = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return result

# Define a dictionary for supported models
SUPPORTED_MODELS = {
    "m2m100": M2M100Translator,
    "marian": MarianTranslator,
    "envt5": EnvT5Translator,
}


class PretrainedModelTranslator(object):

    @staticmethod
    def from_pretrained(model_id: str, config) -> Any:
        """_summary_

        Args:
            type (str): All supported model.
            config (_type_): Configuration of translation (from_lang, to_lang, etc.) and 
                                language model (temperature, num_beams, etc.)

        Raises:
            ValueError: Raised when input type is not valid.

        Returns:
            Any: A Translation tool which is implemented HuggingFace's pretrained model. 
        """
        try:
            if model_id not in SUPPORTED_MODELS:
                raise ValueError(f"{model_id} is not supported. Please try again")
            translator_class = SUPPORTED_MODELS[model_id]
            return translator_class(**config)
        except ValueError: 
            raise ValueError(f"{model_id} is not supported. Please try again")