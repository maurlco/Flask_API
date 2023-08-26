import os

import requests
import torch
from PIL import Image
from flask import Blueprint
from flask import request, jsonify, send_from_directory
from torchvision import transforms, models
from flask import current_app

portrait_api = Blueprint('portrait', __name__,
                         static_folder='static')

MOCKED_PROCESSED_IMAGE_FOLDER= "api/route/static/mock/processed_images"

@portrait_api.route('/')
def index():
    return portrait_api.send_static_file('index.html')

@portrait_api.route('/upload/', methods=['POST'])
def upload_and_predict():

    #1. Receive file upload, validate and store in upload folder
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    filename = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)

    #2. Do the image processing to determine class_name
    input_batch = preprocess_image(filename)
    predicted_class = predict_image_class(input_batch)
    class_name = get_class_name(predicted_class)

    mocked_processed_images_endpoint = f'result_image/{class_name}'

    #4. Send a response here.
    # IN REAL IMPL -
    # We may have store the resulting image (after process) in a Image Storage (S3 AWS?)
    # This would have respond us an image ID, that we can use here to send the Client an
    # image url. This url, (ideally, our backend) would then serve the jpeg file.

    return jsonify({
            'message': 'Image uploaded and processed',
            'predicted_class': predicted_class,
            'class_name': class_name,
            'processed_image_url': f'/{mocked_processed_images_endpoint}'
        })

@portrait_api.route('/processed_images/<filename>')
def processed_image(filename):
    file_path = os.path.join('processed_images', filename)
    print("Processed Image Path:", file_path)
    return portrait_api.send_static_file(file_path)

@portrait_api.route('/result_image/<class_name>')
def processed_image_simple_mock(class_name):
    # Will mock a result, no matter the image_id received (POC version).
    # For real impl, we may for example:
    # 1. check if the user has the authorization
    # 2. Use the image_id to look in the Storage if exist (S3? or others)
    # 3. If valid, call to the (fake url) https://s3server.com/imgs/image_id
    # 4. Respond with the value in call 3.
    #
    # For POC here, we just send a jpeg that we have in the static folder.
    # so we abstract the part with Image storage, user check etc.

    return send_from_directory(MOCKED_PROCESSED_IMAGE_FOLDER,
                               f'processed_{class_name}.jpg',
                               mimetype='image/jpeg')

def preprocess_image(image_path):
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


def predict_image_class(input_batch):
    model = models.mobilenet_v2(pretrained=True)
    model.eval()

    with torch.no_grad():
        output = model(input_batch)

    predicted_class = torch.argmax(output[0]).item()
    return predicted_class


def get_class_name(predicted_class):
    url = "https://s3.amazonaws.com/deep-learning-models/image-models/imagenet_class_index.json"

    # Fetch the class names from the URL
    response = requests.get(url)
    data = response.json()

    # Find the class name corresponding to the predicted class
    if str(predicted_class) in data:
        return data[str(predicted_class)][1]
    else:
        return "Unknown"

