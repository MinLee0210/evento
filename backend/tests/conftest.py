import json
import sys
from pathlib import Path

import numpy as np
import pytest
from fastapi.testclient import TestClient
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

from components.embedders import Embedder  # noqa: E402
from components.ocr_matcher import OcrMatcher  # noqa: E402
from components.query_refiner import QueryRefiner  # noqa: E402
from components.translator import Translator  # noqa: E402
from core.config import Settings  # noqa: E402
from main import create_app  # noqa: E402
from services.keyframes import KeyframeCatalog  # noqa: E402
from services.search import SearchService  # noqa: E402
from services.vector_store import VectorStore  # noqa: E402

KEYFRAMES = [  # (video, frame, shot, ocr)
    ("L01_V001", 10, [0, 50], "breaking news flood"),
    ("L01_V001", 120, [51, 200], None),
    ("L01_V002", 30, [0, 99], "football match score"),
]


class FakeEmbedder(Embedder):
    """Embeds by keyword: each vector is one-hot on the keyframe it names."""

    index_name = "fake"

    def embed_text(self, text):
        return np.eye(len(KEYFRAMES), dtype=np.float32)[[int(text[-1])]]

    def embed_image(self, image):
        return np.eye(len(KEYFRAMES), dtype=np.float32)[[image.getpixel((0, 0))[0]]]


class FakeIndex:
    def __init__(self, vectors):
        self.vectors = vectors

    def search(self, query, k):
        scores = query @ self.vectors.T
        ids = np.argsort(-scores, axis=1)[:, :k]
        return np.take_along_axis(scores, ids, axis=1), ids


class EchoTranslator(Translator):
    def translate(self, text):
        return text


@pytest.fixture
def settings(tmp_path):
    settings = Settings(db_dir=tmp_path)
    settings.keyframes_dir.mkdir()
    settings.media_dir.mkdir()
    rows = ["vid_name|frame|shot|ocr"]
    for i, (video, frame, shot, ocr) in enumerate(KEYFRAMES):
        # Red channel encodes the keyframe id for FakeEmbedder.embed_image.
        Image.new("RGB", (2, 2), (i, 0, 0)).save(settings.keyframes_dir / f"{video}-{frame:05d}.webp", lossless=True)
        rows.append(f"{video}|{frame}|{shot}|{ocr or ''}")
    settings.keyframes_csv.write_text("\n".join(rows))
    urls = {"L01_V001": "https://yt/watch?v=a", "L01_V002": "https://yt/watch?v=b"}
    settings.video_urls_json.write_text(json.dumps(urls))
    settings.url_fps_json.write_text(json.dumps({"https://yt/watch?v=a": 25.0, "https://yt/watch?v=b": 30.0}))
    (settings.media_dir / "L01_V001.json").write_text(json.dumps({"title": "News"}))
    return settings


@pytest.fixture
def service(settings):
    catalog = KeyframeCatalog.from_settings(settings)
    store = VectorStore(FakeIndex(np.eye(len(KEYFRAMES), dtype=np.float32)), FakeEmbedder("cpu"))
    return SearchService(
        catalog=catalog,
        stores=dict.fromkeys(["clip", "blip", "blip_des", "blip_fct"], store),
        translator=EchoTranslator(),
        refiner=QueryRefiner(api_key=None, model_name="unused"),
        ocr=OcrMatcher(catalog.ocr_texts),
    )


@pytest.fixture
def client(service):
    with TestClient(create_app(service)) as client:
        yield client
