from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from .extended_jwt import jwt

ma = Marshmallow()

db = SQLAlchemy()


def init_app(app):
    for ext in [ma,
                db,
                jwt
                ]:
        ext.init_app(app)
