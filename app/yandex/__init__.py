from flask import Blueprint

yandex = Blueprint('yandex', __name__, template_folder='templates')

from . import routes