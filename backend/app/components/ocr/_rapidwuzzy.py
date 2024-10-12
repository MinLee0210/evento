import os
import ast
import glob

import pandas as pd
from rapidfuzz import process as rafu_process, fuzz as rafu_fuzz

from core.config import Config
from components.base import BaseTool


class RapidOCRTool(BaseTool):
    """
    RapidOCRTool class for performing Rapid string matching on OCR text.

    Args:
        csv_path (str): Path to the CSV file containing OCR data.
        mode (int, optional): Rapid matching mode (0 for exact match, 1 for ratio, etc.). Defaults to 0.
        limit (int, optional): Maximum number of matches to return. Defaults to 10.
        separator (str, optional): Separator used in the CSV file. Defaults to "|".
    """

    def __init__(self, csv_path: str, mode: int = 0, limit: int = 10, separator: str = "|"):
        super().__init__()
        self.csv_path = csv_path
        self.mode = mode
        self.limit = limit
        self.separator = separator

        self.keyframes = self.load_keyframes()
        self.imgs_ocr = self.process_ocr()

        self._set_id2img_fps()

    def run(self, input):
        """
        Performs Rapid string matching on OCR text.

        Args:
            input (str): The input text to match.

        Returns:
            list: A list of best matches, each containing the match score and the corresponding OCR text.
        """

        fuzz = [_, rafu_fuzz.ratio, rafu_fuzz.partial_ratio, rafu_fuzz.token_sort_ratio, rafu_fuzz.token_set_ratio, rafu_fuzz.QRatio, rafu_fuzz.WRatio, rafu_fuzz.partial_token_sort_ratio, rafu_fuzz.partial_token_set_ratio]
        best_match = rafu_process.extract(input, self.imgs_ocr, scorer=fuzz[self.mode], limit=self.limit)
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

        env_dir = Config().environment
        lst_keyframes = glob.glob(os.path.join(env_dir.root, env_dir.db_root, f"{env_dir.lst_keyframes['path']}", f"*{env_dir.lst_keyframes['format']}"))
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