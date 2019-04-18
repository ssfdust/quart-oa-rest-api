import asyncio
import warnings
from typing import Any, Optional

from hypercorn.asyncio import serve
from hypercorn.config import Config as HyperConfig
from quart import Quart
from loguru import logger

from .logging import AccessLogger


#  def colored_logger():
#      logger = getLogger('quart.serving')
#      install(level=INFO,
#              logger=logger,
#              fmt='[%(asctime)s] %(message)s')
#
#      return logger
#
#
def filter_func(record):
    prefix = ('quart.app', 'modules', 'quart', 'init')
    if record['name'].startswith(prefix):
        return True
    else:
        return False


def new_logger():
    import sys

    logger.remove(0)
    logger.start(sys.stderr,
                 level='DEBUG',
                 filter=filter_func,
                 format=("<g>{time:YY-MM-DD HH:mm:ss}</g> | "
                         "<e>{name}:{line}</e> | "
                         "<y>{level}</y> | "
                         "<b>{message}</b>"
                         )
                 )

    return logger


class ColoredQuart(Quart):

    def run(
            self,
            host: str = '127.0.0.1',
            port: int = 5000,
            debug: Optional[bool] = None,
            use_reloader: bool = True,
            loop: Optional[asyncio.AbstractEventLoop] = None,
            ca_certs: Optional[str] = None,
            certfile: Optional[str] = None,
            keyfile: Optional[str] = None,
            **kwargs: Any,
    ) -> None:
        """Run this application.

        This is best used for development only, see Hypercorn for
        production servers.

        Arguments:
            host: Hostname to listen on. By default this is loopback
                only, use 0.0.0.0 to have the server listen externally.
            port: Port number to listen on.
            debug: If set enable (or disable) debug mode and debug output.
            use_reloader: Automatically reload on code changes.
            loop: Asyncio loop to create the server in, if None, take default one.
                If specified it is the caller's responsibility to close and cleanup the
                loop.
            ca_certs: Path to the SSL CA certificate file.
            certfile: Path to the SSL certificate file.
            ciphers: Ciphers to use for the SSL setup.
            keyfile: Path to the SSL key file.

        """
        if kwargs:
            warnings.warn(
                f"Additional arguments, {','.join(kwargs.keys())}, are not supported.\n"
                "They may be supported by Hypercorn, which is the ASGI server Quart "
                "uses by default. This method is meant for development and debugging."
            )

        config = HyperConfig()
        config.access_log_format = "{h} | {m} | {s} | {U} | {D}"
        # config.access_logger = colored_logger()
        config.bind = [f"{host}:{port}"]
        config.ca_certs = ca_certs
        config.access_logger_class = AccessLogger
        config.certfile = certfile
        if debug is not None:
            config.debug = debug
        config.error_logger = config.access_logger  # type: ignore
        config.keyfile = keyfile
        config.use_reloader = use_reloader

        scheme = 'https' if config.ssl_enabled else 'http'
        print("Running on {}://{} (CTRL + C to quit)".format(scheme, config.bind[0]))  # noqa: T001

        if loop is not None:
            loop.set_debug(config.debug)
            loop.run_until_complete(serve(self, config))  # type: ignore
        else:
            asyncio.run(serve(self, config), debug=config.debug)  # type: ignore
