from pathlib import Path

import numpy as np
from PIL import Image

from components.embedders import Embedder


class VectorStore:
    """A FAISS index over keyframes, queried through an embedder."""

    def __init__(self, index, embedder: Embedder):
        self.index = index
        self.embedder = embedder

    @classmethod
    def load(cls, features_dir: Path, embedder: Embedder) -> "VectorStore":
        import faiss

        return cls(faiss.read_index(str(features_dir / f"{embedder.index_name}.bin")), embedder)

    def search_text(self, text: str, k: int) -> list[tuple[int, float]]:
        return self._search(self.embedder.embed_text(text), k)

    def search_image(self, image: Image.Image, k: int) -> list[tuple[int, float]]:
        return self._search(self.embedder.embed_image(image), k)

    def _search(self, vector: np.ndarray, k: int) -> list[tuple[int, float]]:
        """Return `(keyframe_id, score)` pairs, best first."""
        scores, ids = self.index.search(vector.astype(np.float32), k)
        return [(int(i), float(s)) for i, s in zip(ids[0], scores[0]) if i >= 0]
