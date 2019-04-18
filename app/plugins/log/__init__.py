from logging import INFO, NOTSET, Logger, getLogger
from typing import TYPE_CHECKING
import loguru
from coloredlogs import install

if TYPE_CHECKING:
    from quart import Quart  # noqa


def create_logger(app: 'Quart') -> Logger:
    """Create a logger for the app based on the app settings.

    This creates a logger named quart.app that has a log level based
    on the app configuration.
    """

    return loguru.logger


def create_serving_logger() -> Logger:
    """Create a logger for serving.

    This creates a logger named quart.serving.
    """
    logger = getLogger('quart.serving')

    if logger.level == NOTSET:
        logger.setLevel(INFO)

    install(INFO, logger=logger)

    return logger
