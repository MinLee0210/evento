"""LLM-based query rewriting ("smart query")."""

import json
from typing import Literal

from typing_extensions import TypedDict

from core.logger import get_logger

RefineMode = Literal["plain", "exploit", "explore"]

EXPLOIT_PROMPT = """Provide a concise and specific search query for an event retrieval engine to find relevant events based on the following prompt. Remember to keep the language and intention of the original prompt.

Prompt: {prompt}

Refine Query:
"""

EXPLORE_PROMPT = """Act as a prompt engineer skilled at refining prompts for an event retrieval engine. Your task is to refine the following prompt to optimize results.  Follow these steps:

1. **Keyword Extraction:** Identify the semantically relevant keywords within the input prompt.  Prioritize keywords that directly relate to events, locations, dates, or key figures.

2. **Contextual Analysis:** Analyze the keywords in relation to the overall topic of the prompt.  Infer the implicit meanings and potential relationships between the keywords.  Consider what specific information the retrieval engine might need to find relevant events.

3. **Refined Prompt Generation:**  Rewrite the input prompt based on your keyword analysis and contextual understanding.  The refined prompt should be a concise and accurate query that explicitly targets the desired information.

Remember to keep the language and intention of the original prompt.

Prompt: {prompt}

Refined Query:
"""


class RefinedQuery(TypedDict):
    refine_response: str


class QueryRefiner:
    """Rewrites a query with Gemini. Falls back to the input on any failure."""

    PROMPTS = {"exploit": EXPLOIT_PROMPT, "explore": EXPLORE_PROMPT}

    def __init__(self, api_key: str | None, model_name: str):
        self.api_key = api_key
        self.model_name = model_name
        self._model = None
        self._log = get_logger()

    def refine(self, query: str, mode: RefineMode = "plain") -> str:
        if mode == "plain":
            return query
        try:
            response = self._get_model().generate_content(
                self.PROMPTS[mode].format(prompt=query),
                generation_config={
                    "response_mime_type": "application/json",
                    "response_schema": RefinedQuery,
                },
            )
            return json.loads(response.text)["refine_response"]
        except Exception:
            self._log.exception("Query refinement (%s) failed; using plain query", mode)
            return query

    def _get_model(self):
        if self._model is None:
            if not self.api_key:
                raise RuntimeError("GOOGLE_API_KEY is not set")
            import google.generativeai as genai

            genai.configure(api_key=self.api_key)
            self._model = genai.GenerativeModel(self.model_name)
        return self._model
