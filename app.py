import sys

from flask import Flask

import route
from dependency_injection import Services
from route.portrait import portrait_api

def create_app():
    #Set up dependency injection
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'uploads'

    container = Services()
    container.wire(modules=[route.portrait])

    # Blueprints
    app.register_blueprint(portrait_api)

    # Start application
    return app


if __name__ == '__main__':
    create_app().run()
