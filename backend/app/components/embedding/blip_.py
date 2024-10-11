from PIL import Image

import torch
from lavis.models import load_model_and_preprocess

from components.base import BaseTool

class BlipTool(BaseTool):
    """
    A tool for extracting features using the BLIP model.

    Args:
        model_name (str, optional): The name of the model to use. Defaults to "blip2_feature_extractor".
        model_type (str, optional): The type of model to use. Defaults to "pretrain".
        is_eval (bool, optional): Whether to use the model in evaluation mode. Defaults to True.
        device (str, optional): The device to use for the model. Defaults to "auto".
    """
    SUPPORTED_MODELS = {
        'blip2': ("blip2_feature_extractor", "blip2fe")
    }
    def __init__(self, model_id: str = "blip2", 
                 model_type: str = "pretrain", 
                 is_eval: bool = True,
                 device: str = "auto"):
        """
        Initializes the BlipTool instance.

        Args:
            model_name (str, optional): The name of the model to use. Defaults to "blip2_feature_extractor".
            model_type (str, optional): The type of model to use. Defaults to "pretrain".
            is_eval (bool, optional): Whether to use the model in evaluation mode. Defaults to True.
            device (str, optional): The device to use for the model. Defaults to "auto".
        """
        super().__init__()
        self.model_name, self.bin_name = self.SUPPORTED_MODELS[model_id]
        self.model, self.image_processor, self.text_processor = load_model_and_preprocess(
            name=self.model_name,
            model_type=model_type,
            is_eval=is_eval,
            device=device
        )
        self.device = device
        
    def run(self, input_data:object, is_numpy:bool=True) -> object:
        """
        Runs the BlipTool on the input data.

        Args:
            input_data (object): The input data to process. Can be a string or a PIL Image.
            is_numpy (bool, optional): Whether the input data is a numpy array. Defaults to True.

        Returns:
            object: The extracted features.

        Raises:
            TypeError: If the input data is not a string or a PIL Image.
        """
        if not isinstance(input_data, (str, Image)):
            raise TypeError("Input data must be a string or a PIL Image.")

        if isinstance(input_data, str):
            features = self._extract_text_features(input_data)
            if is_numpy: 
                features = features.text_embeds_proj[:, 0, :].detach().cpu().numpy()
        elif isinstance(input_data, Image):
            features =  self._extract_by_image_features(input_data)

            if is_numpy: 
                features = features.image_embeds_proj[:, 0, :].detach().cpu().numpy()

        return features
    
    def _extract_text_features(self, text: str) -> object:
        """
        Extracts features from the given text.

        Args:
            text (str): The text to extract features from.

        Returns:
            object: The extracted features.
        """
        with torch.no_grad(): 
            text = self.text_processor['eval'](text)
            text = {"text_input": [text]}
            features = self.model.extract_features(text, mode="text")
        return features

    def _extract_by_image_features(self, image: Image) -> object:
        """
        Extracts features from the given image.

        Args:
            image (Image): The image to extract features from.

        Returns:
            object: The extracted features.
        """
        image = self.image_processor["eval"](image).unsqueeze(0).to(self.device)
        image = {"image": image}
        with torch.no_grad():
            features = self.model.extract_features(image, mode="image")
        return features