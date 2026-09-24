from abc import ABC, abstractmethod


class Translator(ABC):
    def __init__(self, src: str = "vi", dest: str = "en"):
        self.src = src
        self.dest = dest

    @abstractmethod
    def translate(self, text: str) -> str: ...


class GoogleTranslator(Translator):
    def __init__(self, src: str = "vi", dest: str = "en"):
        super().__init__(src, dest)
        import googletrans

        self._client = googletrans.Translator()

    def translate(self, text: str) -> str:
        return self._client.translate(text, src=self.src, dest=self.dest).text
