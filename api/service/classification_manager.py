from werkzeug.datastructures import FileStorage

from service.classification_service import ClassificationService
from service.download_service import DownloadService

class ClassificationManager():
    def __init__(self, download_service: DownloadService, classification_service: ClassificationService):
        self.download_service = download_service
        self.classification_service = classification_service
        pass

    def process(self, file: FileStorage):
        #1. use download service to download the file and get an Image file
        #2. use classification service to get classification name
        #3. Return classification name and Predicted Class number
        pass
