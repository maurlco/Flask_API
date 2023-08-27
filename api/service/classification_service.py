from PIL import Image
import torch

import requests
from torch import Tensor

from torchvision.transforms import transforms
from torchvision import transforms, models

class ClassificationService():

    def predict_class_name(self, file_name: str) -> str:
        input_batch= self._preprocess_image(file_name)
        predicted_class = self._predict_image_class(input_batch)
        return self._get_class_name(predicted_class)


    def _preprocess_image(self, image_path: str) -> Tensor:
        image = Image.open(image_path)
        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        input_tensor = preprocess(image)
        input_batch = input_tensor.unsqueeze(0)
        return input_batch

    def _predict_image_class(self, input_batch: Tensor) -> str:
        model = models.mobilenet_v2(pretrained=True)
        model.eval()

        with torch.no_grad():
            output = model(input_batch)

        predicted_class = torch.argmax(output[0]).item()
        return predicted_class

    def _get_class_name(self, predicted_class):
        url = "https://s3.amazonaws.com/deep-learning-models/image-models/imagenet_class_index.json"

        # Fetch the class names from the URL
        response = requests.get(url)
        data = response.json()

        # Find the class name corresponding to the predicted class
        if str(predicted_class) in data:
            return data[str(predicted_class)][1]
        else:
            return "Unknown"