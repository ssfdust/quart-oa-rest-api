from flask_marshmallow import Marshmallow
from .flask_sqlalchemy import db

from .extended_jwt import jwt
from .logging import Logging

ma = Marshmallow()
logging = Logging()

def init_app(app):
    for ext in [ma,
                db,
                jwt,
                logging
                ]:
        ext.init_app(app)
