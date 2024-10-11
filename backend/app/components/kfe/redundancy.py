import cv2
import torch

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

def color_histogram(img):
    hist = cv2.calcHist([img], [0, 1, 2], None, [8, 8, 8], [0, 255, 0, 255, 0, 255])
    return torch.from_numpy(hist.flatten())

def compute_color_histograms(video, keyframe_indices):
    histograms = []
    for frame_index in keyframe_indices:
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = video.read()
        if ret:
            histograms.append(color_histogram(frame))
    return torch.stack(histograms)

@torch.jit.script
def calculate_similarity_matrix(histograms: torch.Tensor) -> torch.Tensor:
    normalized_histograms = histograms / torch.norm(histograms, dim=1, keepdim=True)
    return torch.mm(normalized_histograms, normalized_histograms.t())

def filter_low_information_frames(histograms: torch.Tensor, keyframe_indices: list[int], threshold: int = 10) -> tuple[torch.Tensor, list[int]]:
    mask = torch.sum(histograms > 0, dim=1) > threshold
    return histograms[mask], [keyframe_indices[i] for i in range(len(keyframe_indices)) if mask[i]]

def remove_redundant_frames(similarity_matrix: torch.Tensor, keyframe_indices: list[int], threshold: float) -> list[int]:
    del_indices = set()
    for i in range(len(keyframe_indices)):
        for j in range(i + 1, len(keyframe_indices)):
            if similarity_matrix[i, j] > threshold:
                del_indices.add(keyframe_indices[j])
    final_indices = set(keyframe_indices) - del_indices
    return sorted(final_indices)

def redundancy_(video, keyframe_indices: list[int], threshold: float = 0.94) -> list[int]:
    histograms = compute_color_histograms(video, keyframe_indices)
    filtered_histograms, filtered_indices = filter_low_information_frames(histograms, keyframe_indices)
    similarity_matrix = calculate_similarity_matrix(filtered_histograms)
    final_indices = remove_redundant_frames(similarity_matrix, filtered_indices, threshold)
    return final_indices