from werkzeug.datastructures import FileStorage

from service.classification_service import ClassificationService
from service.download_service import DownloadService

class ClassificationManager():
    def __init__(self, download_service: DownloadService, classification_service: ClassificationService):
        self.download_service = download_service
        self.classification_service = classification_service

    def compute_class_name(self, file: FileStorage) -> str:
        stored_file_path = self.download_service.store(file)
        class_name = self.classification_service.predict_class_name(stored_file_path)

        return class_name
