import underthesea
from pyvi import ViUtils, ViTokenizer
from difflib import SequenceMatcher
from langdetect import detect

class Text_Preprocessing:
    def __init__(self, stopwords_path='./dict/vietnamese-stopwords-dash.txt'):
        with open(stopwords_path, 'rb') as f:
            lines = f.readlines()
        self.stop_words = [line.decode('utf8').strip() for line in lines]

    def remove_stopwords(self, text):
        text = ViTokenizer.tokenize(text)
        return " ".join([w for w in text.split() if w not in self.stop_words])

    def lowercasing(self, text):
        return text.lower()

    def text_norm(self, text):
        return underthesea.text_normalize(text)

    def text_classify(self, text):
        return underthesea.classify(text)

    def __call__(self, text):
        text = self.lowercasing(text)
        text = self.remove_stopwords(text)
        text = self.text_norm(text)
        categories = self.text_classify(text)
        return categories
