import os
import sys
import json
import yaml
import warnings
from pathlib import Path


def read_yaml(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}")
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML: {e}")


def json_to_str(payload: dict) -> str:
    return json.dumps(payload)


def str_to_json(payload: str) -> dict:
    try:
        return json.loads(payload)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON string: {e}")


# TODO: Improve this to act as `dynamic_dirname`
def get_to_root():
    """
    Retrieves the root directory of the current script.

    Returns:
        Path: The root directory path.
    """

    FILE = Path(__file__).resolve()  # Resolves the absolute path of the current script
    ROOT = FILE.parents[1]  # Navigates one directory up from the script's directory to find the root

    if str(ROOT) not in sys.path:
        sys.path.append(str(ROOT))  # Adds the root directory to the system path for module import

    ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # Makes the root path relative to the current working directory

    return ROOT


def dynamic_dirname(path, depth):
    """
    Recursively traverses the directory path to the specified depth.

    Args:
        path (str): The starting path.
        depth (int): The desired depth to traverse.

    Returns:
        str: The directory path at the specified depth.

    Example: 

        current_dir = os.path.dirname(__file__)
        desired_depth = 3  # Adjust the depth as needed

        result = dynamic_dirname(current_dir, desired_depth)
        print(result)  # Output: ./HCMC-AIO2024
    """

    if depth == 0:
        return path

    parent_dir = os.path.dirname(path)
    return dynamic_dirname(parent_dir, depth - 1)


def ignore_warning():
    warnings.filterwarnings("ignore")