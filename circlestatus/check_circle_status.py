import requests
import sys
import time
import logger_config

config = logger_config.get_config_parser()

log_name = config.get('override', 'log_name')
log_level = config.get('override', 'log_level')
config_json_attempts = config.get('override', 'json_attempts')
config_poll_tries = config.get('override', 'poll_tries')
sleep_time = config.get('override', 'sleep_time')

logger = logger_config.init_a_logger(log_name, log_level)
# Pass in circleci environment variable from a pipeline repo
circle_link = sys.argv[1]
response_limit = '1'


def circle_request():
    r = ''
    json_attempts = config_json_attempts

    try:
        while json_attempts > 0:
            r = requests.get('{}&limit={}'.format(circle_link, response_limit))
            if r.status_code != 200:
                json_attempts -= 1
            else:
                r = r.json()[0]
                break
    except Exception:
        logger.error('request.get() or while loop failed')
    return r


def circle_status():
    poll_tries = config_poll_tries
    build = circle_request()

    while poll_tries > 0:
        if build['lifecycle'] == 'running' and build['outcome'] is None:
            time.sleep(sleep_time)
            poll_tries -= 1
            build = circle_request()
        else:
            return 'kicking off pipeline controller'

    if poll_tries == 0:
        logger.warning('Ran out of tries!')
        sys.exit(1)

if __name__ == '__main__':
    circle_status()
