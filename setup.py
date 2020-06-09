import logging
from config import DevConfig


# configure logger
def get_logger():
    logging.basicConfig(filename=DevConfig.LOGGER_FILE, level=DevConfig.LOG_LEVEL, format=DevConfig.LOG_FORMAT)
    return logging.getLogger()


logger = get_logger()