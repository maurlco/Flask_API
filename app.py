import os

from flask import Flask
from flask_injector import FlaskInjector
from app_module import AppModule
from route.portrait import portrait_api

def create_app():
    app = Flask(__name__)
    #configs
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
    # Blueprints
    app.register_blueprint(portrait_api)

    # Set up the dependency injection
    FlaskInjector(app=app,
                  # All XXModule classes that we created...
                  modules=[AppModule])

    return app

if __name__ == '__main__':
    create_app().run()
