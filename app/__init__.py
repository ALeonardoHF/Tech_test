from flask import Flask
from .yandex import yandex



def run():
    app = Flask(__name__)
    app.register_blueprint(yandex)

    return app