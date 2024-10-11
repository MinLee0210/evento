"""Define class for extracting keyframes from a video.
"""
import torch
import numpy as np

from src.tools.kfe.k_means import kmeans_silhouette
from src.tools.kfe.redundancy import redundancy_

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

# TODO: Call TransNetV2

def keyframe_extraction(shot: tuple[int, int], features: np.ndarray, video, threshold: float = 0.94) -> list[int]:
    start, _ = shot
    features_tensor = torch.as_tensor(features, device=DEVICE, dtype=torch.float32)
    _, _, _, index = kmeans_silhouette(features_tensor)
    final_index = [start + i for i in index]
    keyframe_index = redundancy_(video, final_index, threshold)
    return sorted(keyframe_index)