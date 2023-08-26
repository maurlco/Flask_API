from flask import Flask

from route.portrait import portrait_api

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

app.register_blueprint(portrait_api)

if __name__ == '__main__':
    app.run()
