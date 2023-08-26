from service.classification_service import ClassificationService
from service.download_service import DownloadService

class ClassificationManager():
    def __init__(self, download_service: DownloadService, classification_service: ClassificationService):
        print("I am Classification Manager and I am born")
        pass

    def prout(self):
        print("prout")