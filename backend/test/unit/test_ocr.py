import unittest

from backend.app.components.fuzzymatching import OCRFactory


class TestOCR(unittest.TestCase):
    def setUp(self):
        config = {"csv_path": "./backend/db/keyframes.csv"}
        self.ocr_matcher = OCRFactory.produce("fuzzywuzzy", config)

    def test_search_by_keywords(self):
        keyword = "Apple"
        result = self.ocr_matcher.run(keyword)
        self.assertIsInstance(result, list)
