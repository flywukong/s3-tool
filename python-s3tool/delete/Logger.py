import logging
from logging.handlers import RotatingFileHandler


def getLogger(filename):
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    fh = RotatingFileHandler(filename, maxBytes=100*1024*1024)
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s][%(filename)s][%(lineno)d][%(levelname)s] %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger
