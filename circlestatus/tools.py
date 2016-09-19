import logging
import os
from ConfigParser import ConfigParser

WORKING_DIR = os.path.abspath(os.path.dirname(__file__))
CONFIG_FILE = WORKING_DIR + "/config"

#  to enable testing we should make a dynamic path available
config = ConfigParser()
config.read(CONFIG_FILE)


def init_a_logger():

    log_name = config.get('override', 'log_name')
    log_level = config.get('override', 'log_level')
    # create logger
    logger = logging.Logger(log_name)
    logger.setLevel(log_level)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(log_level)

    # create formatter to hx standard
    formatter = logging.Formatter('%(asctime)s - %(name)s '
                                  '- %(levelname)s %(module)s:%(lineno)s '
                                  '%(funcName)s - %(message)s')
    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    return logger


def get_config_variables():
    config_json_attempts = config.get('override', 'json_attempts')
    config_poll_tries = config.get('override', 'poll_tries')
    sleep_time = config.get('override', 'sleep_time')
    response_limit = config.get('override', 'response_limit')

    return config_json_attempts, config_poll_tries, sleep_time, response_limit
