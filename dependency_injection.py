from dependency_injector import containers, providers
from flask import Flask

from service.classification_manager import ClassificationManager
from service.classification_service import ClassificationService
from service.download_service import DownloadService


class Services(containers.DeclarativeContainer):
    download_service = providers.Singleton(DownloadService)
    classification_service = providers.Singleton(ClassificationService)
    classification_manager_instance = ClassificationManager(download_service(),
                                                            classification_service())

    classification_manager = providers.Object(classification_manager_instance)

