import unittest
import requests
import torch
from PIL import Image

from lavis.models import load_model_and_preprocess

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class TestBlip2(unittest.TestCase):
    def setUp(self): 
        self.model, self.vis_processors, self.txt_processors = load_model_and_preprocess(name="blip2_feature_extractor", 
                                                                  model_type="pretrain", 
                                                                  is_eval=True, 
                                                                  device=device
                                                                  )
        
    def test_similar_features(self): 
        # setup device to use

        # load sample image
        image_url = "https://cdn.shopify.com/s/files/1/0910/2272/files/vers_large.jpg"
        image_response = requests.get(image_url)

        raw_image = Image.open(requests.get(image_url, stream = True).raw)

        caption = "a large fountain spewing water into the air"
        image = self.vis_processors["eval"](raw_image).unsqueeze(0).to(device)
        text_input = self.txt_processors["eval"](caption)
        sample = {"image": image, "text_input": [text_input]}

        features_multimodal = self.model.extract_features(sample)
        # torch.Size([1, 12, 768]), use features_multimodal[:,0,:] for multimodal classification tasks

        features_image = self.model.extract_features(sample, mode="image")  # torch.Size([1, 197, 768])
        features_text = self.model.extract_features(sample, mode="text")    # torch.Size([1, 12, 768])

        # low-dimensional projected features: 
        #       image: torch.Size([1, 197, 256])
        #       text: # torch.Size([1, 12, 256])
                
        similarity = features_image.image_embeds_proj[:,0,:] @ features_text.text_embeds_proj[:,0,:].t()
        self.assertIsInstance(similarity, torch.Tensor)