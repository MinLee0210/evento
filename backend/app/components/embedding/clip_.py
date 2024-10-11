from PIL import Image

from transformers import CLIPModel, CLIPImageProcessor, CLIPTokenizer

from components.base import BaseTool

class ClipTool(BaseTool): 

    SUPPORTED_MODELS = {
    "clipB32": ("openai/clip-vit-base-patch32", 'clipB32'),
    "metaB16": ("facebook/metaclip-b16-fullcc2.5b", 'metaB16'),
    "metaL14": ('facebook/metaclip-l14-fullcc2.5b', 'metaL14'),
    "metaH14": ('facebook/metaclip-h14-fullcc2.5b', 'metaH14')
    }

    def __init__(self, model_id:str="clipB32", device:str="auto") -> None:
        super().__init__()

        # TODO: change model_name -> model_id for uniquity in naming.
        self.model_name, self.bin_name = self.SUPPORTED_MODELS[model_id]
        self.model = CLIPModel.from_pretrained(self.model_name).to(self.device)
        self.image_processor = CLIPImageProcessor.from_pretrained(self.model_name)
        self.text_processor = CLIPTokenizer.from_pretrained(self.model_name)
        self.device = device

    def run(self, input_data: object, is_numpy: bool = True) -> object:
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
        elif isinstance(input_data, Image):
            features =  self._extract_by_image_features(input_data)

        if is_numpy: 
            features = features.detach().cpu().numpy()

        return features

    def _extract_text_features(self, text: str) -> object:
        """
        Extracts features from the given text.

        Args:
            text (str): The text to extract features from.

        Returns:
            object: The extracted features.
        """
        text = self.text_processor([text], return_tensors="pt").to(self.device)
        result =  self.model.get_text_features(**text)
        return result

    def _extract_by_image_features(self, image: Image) -> object:
        """
        Extracts features from the given image.

        Args:
            image (Image): The image to extract features from.

        Returns:
            object: The extracted features.
        """
        image = self.image_processor(images=image, return_tensors="pt").to(self.device)
        features = self.model.extract_features(**image, mode="image")
        return features