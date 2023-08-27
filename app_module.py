from injector import Module, provider, singleton

from service.classification_manager import ClassificationManager
from service.classification_service import ClassificationService
from service.download_service import DownloadService


'''
App Module is to create all the singletons
'''
class AppModule(Module):
    @provider
    @singleton
    def classification_service(self) -> ClassificationService:
        return ClassificationService()

    def download_service(self) -> DownloadService:
        return DownloadService()

    @provider
    @singleton
    def classification_manager(self,
                                classification_service: ClassificationService,
                                download_service: DownloadService) -> ClassificationManager:
        return ClassificationManager(download_service, classification_service)