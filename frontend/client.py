import requests
import streamlit as st


class BackendClient:
    """Thin HTTP client for the evento backend."""

    def __init__(self, base_url: str, timeout: float = 60):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def search(self, query: str, top_k: int, model: str, smart_query: str) -> list[dict]:
        return _post(
            f"{self.base_url}/search/",
            {"query": query, "top_k": top_k, "high_performance": model, "smart_query": smart_query},
            self.timeout,
        )

    def search_ocr(self, query: str, top_k: int, mode: int) -> list[dict]:
        return _post(
            f"{self.base_url}/search/ocr",
            {"query": query, "top_k": top_k, "mode": mode},
            self.timeout,
        )

    def image_url(self, image: str) -> str:
        return f"{self.base_url}/search/image/{image}"


@st.cache_data(show_spinner=False)
def _post(url: str, payload: dict, timeout: float) -> list[dict]:
    response = requests.post(url, json=payload, timeout=timeout)
    if not response.ok:
        raise RuntimeError(f"{response.status_code}: {response.text}")
    return response.json()["hits"]
