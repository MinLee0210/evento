"""Text/image encoders that map queries into the FAISS feature space."""

from abc import ABC, abstractmethod

import numpy as np
from PIL import Image


class Embedder(ABC):
    """Encodes text and images into row vectors of shape (1, dim)."""

    #: Stem of the FAISS index file in `db/features` built with this encoder.
    index_name: str

    def __init__(self, device: str):
        self.device = device

    @abstractmethod
    def embed_text(self, text: str) -> np.ndarray: ...

    @abstractmethod
    def embed_image(self, image: Image.Image) -> np.ndarray: ...


class ClipEmbedder(Embedder):
    index_name = "clipB32"
    model_id = "openai/clip-vit-base-patch32"

    def __init__(self, device: str):
        super().__init__(device)
        from transformers import CLIPModel, CLIPProcessor

        self.model = CLIPModel.from_pretrained(self.model_id).to(device).eval()
        self.processor = CLIPProcessor.from_pretrained(self.model_id)

    def embed_text(self, text: str) -> np.ndarray:
        inputs = self.processor(text=[text], return_tensors="pt").to(self.device)
        return self._encode(self.model.get_text_features, inputs)

    def embed_image(self, image: Image.Image) -> np.ndarray:
        inputs = self.processor(images=image, return_tensors="pt").to(self.device)
        return self._encode(self.model.get_image_features, inputs)

    @staticmethod
    def _encode(fn, inputs) -> np.ndarray:
        import torch

        with torch.inference_mode():
            return fn(**inputs).cpu().numpy()


class BlipEmbedder(Embedder):
    index_name = "blip2fe_img"

    def __init__(self, device: str):
        super().__init__(device)
        from lavis.models import load_model_and_preprocess

        self.model, self.image_processor, self.text_processor = load_model_and_preprocess(
            name="blip2_feature_extractor",
            model_type="pretrain",
            is_eval=True,
            device=device,
        )

    def embed_text(self, text: str) -> np.ndarray:
        sample = {"text_input": [self.text_processor["eval"](text)]}
        return self._encode(sample, "text").text_embeds_proj[:, 0, :].cpu().numpy()

    def embed_image(self, image: Image.Image) -> np.ndarray:
        tensor = self.image_processor["eval"](image.convert("RGB")).unsqueeze(0)
        sample = {"image": tensor.to(self.device)}
        return self._encode(sample, "image").image_embeds_proj[:, 0, :].cpu().numpy()

    def _encode(self, sample: dict, mode: str):
        import torch

        with torch.inference_mode():
            return self.model.extract_features(sample, mode=mode)
