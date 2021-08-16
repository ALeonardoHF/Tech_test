from flask import Flask
# import requests
from .yandex import yandex



def run():
    app = Flask(__name__)
    app.register_blueprint(yandex)
    app.secret_key = 'S3CR3TK3Y'
    # app.jinja_env.add_extensions('jinja2.ext.loopcontrols')

    return app