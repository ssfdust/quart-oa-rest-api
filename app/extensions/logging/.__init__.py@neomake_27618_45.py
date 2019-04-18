from loguru import logger


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
