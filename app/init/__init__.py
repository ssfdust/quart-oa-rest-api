from extensions.colored_quart import ColoredQuart as Quart
from modules.auth import blp as auth_blp
from extensions import init_app
from config import BaseConfig

def create_app():
    app = Quart(__name__)
    app.config.from_object(BaseConfig)

    init_app(app)
    app.register_blueprint(auth_blp)

    return app
