import json

import streamlit as st
import streamlit.components.v1 as components

from client import BackendClient

DEFAULT_BACKEND_URL = "http://103.20.97.119:8080"
QUERY_HINT = 'Eg: "Cảnh quay một chiếc thuyền cứu hộ đi trên băng..." || "L01_V001, 1" || "https://bitexco.c...scaled.jpg"'
GRID_COLUMNS = 4


class SearchState:
    """Typed view over `st.session_state` for this page."""

    def __init__(self):
        st.session_state.setdefault("hits", [])
        st.session_state.setdefault("focused", None)  # hit shown in "Video details"
        st.session_state.setdefault("selected", {})  # "video, frame" -> hit
        st.session_state.setdefault("clipboard", None)

    @property
    def hits(self) -> list[dict]:
        return st.session_state["hits"]

    @hits.setter
    def hits(self, hits: list[dict]):
        st.session_state["hits"] = hits
        st.session_state["selected"] = {}

    @property
    def focused(self) -> dict | None:
        return st.session_state["focused"]

    @property
    def selected(self) -> dict[str, dict]:
        return st.session_state["selected"]

    def focus(self, hit: dict):
        st.session_state["focused"] = hit
        st.session_state["clipboard"] = label(hit)

    def set_selected(self, hit: dict, selected: bool):
        if selected:
            self.selected[label(hit)] = hit
        else:
            self.selected.pop(label(hit), None)

    def pop_clipboard(self) -> str | None:
        text, st.session_state["clipboard"] = st.session_state["clipboard"], None
        return text


def label(hit: dict) -> str:
    return f"{hit['video']}, {hit['frame']}"


class SearchPage:
    def __init__(self):
        self.state = SearchState()
        with st.sidebar:
            self.client = BackendClient(st.text_input("Input backend url", value=DEFAULT_BACKEND_URL))
            st.write("---")
            st.write("App created by **AIO_TOP10**")

    def render(self):
        st.markdown("<h1 style='text-align: center;'>Image Retrieval System - AIC2024</h1>", unsafe_allow_html=True)
        left, right = st.columns([1, 2])
        with left:
            self._render_details()
            self._render_selection()
        with right:
            self._render_search()
            self._render_grid()
        self._copy_to_clipboard()

    # ---- left column ----
    def _render_details(self):
        with st.expander("Video details"):
            hit = self.state.focused
            if not hit:
                st.write("No video selected.")
                return
            st.video(hit["url"])
            second = int(hit["url"].rsplit("&t=", 1)[1])
            st.write(f"**Video ID:** {hit['video']}, {second * 1000}")
            st.write(f"**Video ID:** {label(hit)}")
            st.write(f"**Video URL:** {hit['url']}")
            self._select_checkbox(hit, "details")

    def _render_selection(self):
        with st.expander("Selected image(s)"):
            if not self.state.selected:
                st.write("No images selected.")
            for name in self.state.selected:
                st.write(f"**{name}**")

    # ---- right column ----
    def _render_search(self):
        text_tab, ocr_tab = st.tabs(["Sentence-based search", "OCR-based search"])
        with text_tab:
            with st.expander("Settings"):
                top_k = self._top_k_slider("text")
                model = st.select_slider(
                    "You can choose CLIP-based or BLIP-based",
                    options=["BLIP", "BLIP_DES", "BLIP_FCT", "CLIP"],
                    value="BLIP",
                ).lower()
                smart_query = st.select_slider(
                    "You can choose method to augment query.",
                    options=["Plain", "Explore", "Exploit"],
                    value="Plain",
                ).lower()
            query = st.text_input("Enter a text query, a frame or an image url", placeholder=QUERY_HINT)
            if st.button("Search", key="text_search") and query:
                self._run(self.client.search, query, top_k, model, smart_query)

        with ocr_tab:
            with st.expander("Settings"):
                top_k = self._top_k_slider("ocr")
                mode = st.slider(
                    "Mode of algorithm",
                    min_value=0,
                    max_value=7,
                    help="Adjust mode the change the fuzzy matching algorithm.",
                )
            query = st.text_input("Enter a keyword", placeholder=QUERY_HINT)
            if st.button("Search", key="ocr_search") and query:
                self._run(self.client.search_ocr, query, top_k, mode)

    def _render_grid(self):
        hits = self.state.hits
        for start in range(0, len(hits), GRID_COLUMNS):
            row = hits[start : start + GRID_COLUMNS]
            for col, hit in zip(st.columns(len(row)), row):
                with col:
                    st.image(self.client.image_url(hit["image"]))
                    st.button(label(hit), key=f"btn_{hit['image']}", on_click=self.state.focus, args=(hit,))
                    self._select_checkbox(hit, "grid")

    # ---- helpers ----
    def _run(self, search, *args):
        with st.spinner("Performing search..."):
            try:
                self.state.hits = search(*args)
            except Exception as e:
                st.error(e)

    def _select_checkbox(self, hit: dict, where: str):
        # Seed from the selection so the details and grid checkboxes stay in sync.
        key = f"select_{where}_{hit['image']}"
        st.session_state[key] = label(hit) in self.state.selected
        st.checkbox("Select", key=key, on_change=lambda: self.state.set_selected(hit, st.session_state[key]))

    @staticmethod
    def _top_k_slider(key: str) -> int:
        return st.slider(
            "Number of Neighbors (K_neighbors)",
            min_value=10,
            max_value=1000,
            value=100,
            step=10,
            help="Adjust the number of nearest neighbors to retrieve.",
            key=f"top_k_{key}",
        )

    def _copy_to_clipboard(self):
        if text := self.state.pop_clipboard():
            components.html(f"<script>navigator.clipboard.writeText({json.dumps(text)});</script>", height=0)
