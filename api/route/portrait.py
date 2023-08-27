import os
from injector import inject
from flask import Blueprint
from flask import request, jsonify, send_from_directory
from flask import current_app

from service.classification_manager import ClassificationManager

portrait_api = Blueprint('portrait', __name__,
                         static_folder='static')

MOCKED_PROCESSED_IMAGE_FOLDER = "api/route/static/mock/processed_images"

@portrait_api.route('/')
def index():
    return portrait_api.send_static_file('index.html')

@portrait_api.route('/upload/', methods=['POST'])
@inject
def upload_and_predict(classification_manager: ClassificationManager):
    # IN REAL IMPL -
    # We may have store the resulting image (after process) in a Image Storage (S3 AWS?)
    # This would have respond us an image ID, that we can use here to send the Client an
    # image url. This url, (ideally, our backend) would then serve the jpeg file.

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    class_name = classification_manager.compute_class_name(file)

    return jsonify({
            'message': 'Image uploaded and processed',
            'class_name': class_name
        })





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
