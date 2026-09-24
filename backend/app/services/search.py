import re
from io import BytesIO

import requests
from PIL import Image

from components.embedders import BlipEmbedder, ClipEmbedder
from components.ocr_matcher import OcrMatcher
from components.query_refiner import QueryRefiner
from components.translator import GoogleTranslator, Translator
from core.config import Settings
from core.logger import get_logger
from schema.search import Hit, OcrSearchRequest, TextSearchRequest
from services.keyframes import KeyframeCatalog
from services.vector_store import VectorStore

URL = re.compile(r"^https?://\S+$")


class SearchService:
    """Entry point for every search mode: text, image URL, frame reference and OCR."""

    def __init__(
        self,
        catalog: KeyframeCatalog,
        stores: dict[str, VectorStore],
        translator: Translator,
        refiner: QueryRefiner,
        ocr: OcrMatcher,
    ):
        self.catalog = catalog
        self.stores = stores
        self.translator = translator
        self.refiner = refiner
        self.ocr = ocr
        self._log = get_logger()

    @classmethod
    def from_settings(cls, settings: Settings) -> "SearchService":
        catalog = KeyframeCatalog.from_settings(settings)
        clip = VectorStore.load(settings.features_dir, ClipEmbedder(settings.device))
        blip = VectorStore.load(settings.features_dir, BlipEmbedder(settings.device))
        return cls(
            catalog=catalog,
            # The BLIP variants have always shared one model and one index.
            stores={"clip": clip, "blip": blip, "blip_des": blip, "blip_fct": blip},
            translator=GoogleTranslator(),
            refiner=QueryRefiner(settings.google_api_key, settings.gemini_model),
            ocr=OcrMatcher(catalog.ocr_texts),
        )

    def search(self, request: TextSearchRequest) -> list[Hit]:
        store = self.stores[request.high_performance]
        query = request.query.strip()

        if URL.match(query):
            self._log.info("Image-URL search: %s", query)
            results = store.search_image(self._download_image(query), request.top_k)
        elif ref := self.catalog.parse_frame_ref(query):
            self._log.info("Frame search: %s", ref)
            image = Image.open(self.catalog.closest_keyframe(*ref))
            results = store.search_image(image, request.top_k)
        else:
            text = self.refiner.refine(self.translator.translate(query), request.smart_query)
            self._log.info("Text search: %r -> %r", query, text)
            results = store.search_text(text, request.top_k)

        return [self.catalog.hit(i, score) for i, score in results]

    def search_ocr(self, request: OcrSearchRequest) -> list[Hit]:
        results = self.ocr.match(request.query, request.top_k, request.mode)
        return [self.catalog.hit(i, score) for i, score in results]

    @staticmethod
    def _download_image(url: str) -> Image.Image:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return Image.open(BytesIO(response.content)).convert("RGB")
