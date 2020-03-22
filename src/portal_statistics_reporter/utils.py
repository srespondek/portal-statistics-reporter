import logging
import os


def get_logger(name=__name__):
    logger = logging.getLogger(name)

    if bool(os.getenv('ENABLE_DEBUG_LOGGING', False)):
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    return logger