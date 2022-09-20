import logging
from helpers.CustomFormatter import CustomFormatter

class Logger:

    def log():
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        fmt = '[ %(levelname)s ] > %(message)s'

        stdout_handler = logging.StreamHandler()
        stdout_handler.setLevel(logging.DEBUG)
        stdout_handler.setFormatter(CustomFormatter(fmt))

        logger.addHandler(stdout_handler)

        return logger

