import os

from flask import current_app, request
from werkzeug.datastructures import FileStorage


class DownloadService:

    def store(self, file: FileStorage) -> str:
        filename = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        return filename
