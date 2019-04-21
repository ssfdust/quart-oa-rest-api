from quart import Blueprint

blp = Blueprint('auth', __name__, url_prefix='/auth')

from .resources import *  # noqa
