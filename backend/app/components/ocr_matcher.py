from collections.abc import Sequence

from rapidfuzz import fuzz, process


class OcrMatcher:
    """Fuzzy-matches a keyword against the OCR text of every keyframe."""

    SCORERS = (
        fuzz.ratio,
        fuzz.partial_ratio,
        fuzz.token_sort_ratio,
        fuzz.token_set_ratio,
        fuzz.QRatio,
        fuzz.WRatio,
        fuzz.partial_token_sort_ratio,
        fuzz.partial_token_set_ratio,
    )

    def __init__(self, texts: Sequence[str | None]):
        # Keys are keyframe ids; None entries are skipped by rapidfuzz.
        self._texts = dict(enumerate(texts))

    def match(self, query: str, top_k: int, mode: int = 0) -> list[tuple[int, float]]:
        """Return `(keyframe_id, score)` pairs, best first."""
        scorer = self.SCORERS[mode]
        results = process.extract(query, self._texts, scorer=scorer, limit=top_k)
        return [(key, score) for _, score, key in results]
