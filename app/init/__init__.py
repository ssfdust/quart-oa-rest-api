from extensions.colored_quart import ColoredQuart as Quart
from modules.auth import blp as auth_blp


def create_app():
    app = Quart(__name__)

    app.register_blueprint(auth_blp)

    return app
