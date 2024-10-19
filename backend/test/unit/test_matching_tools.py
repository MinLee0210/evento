import json
import os
import unittest

from dotenv import load_dotenv

from app.components.fuzzymatching import FuzzyMatchingFactory
from app.components.llms import AgentFactory
from app.components.llms.prompts import EXTRACT_KEYWORDS

load_dotenv()


class TestMatchingTools(unittest.TestCase):
    def setUp(self):
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

        llm_config = {"api_key": GOOGLE_API_KEY}
        self.llm_agent = AgentFactory.produce(provider="gemini", **llm_config)

        config = {"csv_path": "./backend/db/keyframes.csv"}
        self.ocr_matcher = FuzzyMatchingFactory.produce("rapidwuzzy", **config)

    def test_matching(self, query):
        "Extracting keywords from query and return a list of videos that are relevant to those keywords"
        keywords = self.llm_agent.run(EXTRACT_KEYWORDS + "\n" + query)
        keywords = json.loads(keywords)
        keywords = [d["keyword"] for d in keywords]

        matching_paths = []

        for kw in keywords:
            result = self.ocr_matcher.run(kw)
            img_paths = self.ocr_matcher.get_image_paths(result)
            matching_paths += img_paths

        matching_paths = list(set(matching_paths))

        # At this moment, just check if it returns the right type.
        self.assertIsInstance(matching_paths, list)
