import os
import ast
import glob

import pandas as pd
from fuzzywuzzy import process as fuwu_process, fuzz as fuwu_fuzz

from core.config import Config
from components.base import BaseTool


class FuzzyMatchingTool(BaseTool):
    """
    FuzzyOCRTool class for performing fuzzy string matching on OCR text.

    Args:
        csv_path (str): Path to the CSV file containing OCR data.
        mode (int, optional): Fuzzy matching mode (0 for exact match, 1 for ratio, etc.). Defaults to 0.
        limit (int, optional): Maximum number of matches to return. Defaults to 10.
        separator (str, optional): Separator used in the CSV file. Defaults to "|".
    """

    def __init__(self, csv_path: str, mode: int = 0, limit: int = 10, separator: str = "|"):
        super().__init__()
        self.env_dir = Config().environment
        # self.csv_path = csv_path
        self.csv_path = os.path.join(self.env_dir.root, self.env_dir.db_root, self.env_dir.keyframes)
        self.mode = mode
        self.limit = limit
        self.separator = separator

        self.keyframes = self.load_keyframes()
        self.imgs_ocr = self.process_ocr()

        self._set_id2img_fps()

    def run(self, input):
        """
        Performs fuzzy string matching on OCR text.

        Args:
            input (str): The input text to match.

        Returns:
            list: A list of best matches, each containing the match score and the corresponding OCR text.
        """

        fuzz = [fuwu_fuzz.ratio, fuwu_fuzz.partial_ratio, fuwu_fuzz.token_sort_ratio, fuwu_fuzz.token_set_ratio, fuwu_fuzz.QRatio, fuwu_fuzz.WRatio]
        best_match = fuwu_process.extract(input, self.imgs_ocr, scorer=fuzz[self.mode], limit=self.limit)
        return best_match

    def load_keyframes(self):
        """
        Loads keyframes data from a CSV file.

        Returns:
            pandas.DataFrame: A DataFrame containing keyframes data.
        """

        return pd.read_csv(self.csv_path, sep=self.separator)

    def process_ocr(self):
        """
        Processes OCR text data from the keyframes DataFrame.

        Returns:
            dict: A dictionary mapping keyframe IDs to OCR text.
        """

        imgs_ocr = self.keyframes['ocr'].to_dict()
        return {
            key: ' '.join(ast.literal_eval(value)) if pd.notna(value) else ''
            for key, value in imgs_ocr.items()
        }

    def _set_id2img_fps(self):
        """
        Sets a mapping between keyframe IDs and image file paths.
        """
        lst_keyframes = glob.glob(os.path.join(self.env_dir.root, self.env_dir.db_root, f"{self.env_dir.lst_keyframes['path']}", f"*{self.env_dir.lst_keyframes['format']}"))
        lst_keyframes.sort()

        self.id2img_fps = {i: img_path for i, img_path in enumerate(lst_keyframes)}

    def get_image_paths(self, best_matches):
        """
        Gets the image file paths corresponding to the best matches.

        Args:
            best_matches (list): A list of best match tuples.

        Returns:
            list: A list of image file paths.
        """

        return [self.id2img_fps[img[-1]] for img in best_matches]