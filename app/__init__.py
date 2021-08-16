from flask import Flask
from .yandex import yandex
from .test import test



def run():
    app = Flask(__name__)
    app.register_blueprint(yandex)
    app.register_blueprint(test)

    return app