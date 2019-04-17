from quart import Quart
from loguru import logger
from logging import getLogger
from coloredlogs import install

def create_app():
    app = Quart(__name__)
    logger.info('Program starting...')
    register_logger(app)
    app.before_first_request(remove_handler)

    return app

def remove_handler():
    server_logger = getLogger('quart.serving')
    server_logger.handlers.pop()
    install(level=None, logger=server_logger)

def register_logger(app):
    app._logger = logger
