import logging
import os
from . import  constants

if not constants.LOG_PATH.exists():
    constants.LOG_PATH.mkdir()


LOGGER_LEVEL = logging.INFO
LOG = None

def get_logging_filename():
    return constants.LOG_PATH.joinpath("running.log").absolute().as_posix()

def setup_logging_level():
    global LOGGER_LEVEL
    try:
        level = str(os.environ[constants.LOG_ENV_KEY]).strip()
        if level == "ERROR":
            LOGGER_LEVEL = logging.ERROR
        elif level == "WARNING":
            LOGGER_LEVEL = logging.WARNING
        elif level == "INFO":
            LOGGER_LEVEL = logging.INFO
        elif level == "DEBUG":
            print("setting to debug")
            LOGGER_LEVEL = logging.DEBUG
        else:
            raise ValueError("invalid logger level: {0!r}".format(level))
    except KeyError:
        print("failed to get env key: {} for logging ".format(constants.LOG_ENV_KEY))
        print("setting default logging level to {}".format(LOGGER_LEVEL))

def setup_logger():
    global LOG, LOGGER_LEVEL
    setup_logging_level()
    # create logger with 'spam_application'
    logger = logging.getLogger('dianping_digger')
    logger.setLevel(LOGGER_LEVEL)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(get_logging_filename(), mode="a+")
    fh.setLevel(LOGGER_LEVEL)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(LOGGER_LEVEL)
    # create formatter and add it to the handlers
    formatter = logging.Formatter("- %(levelname)s | %(module)s | %(asctime)s -: %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    LOG = logger


setup_logger()