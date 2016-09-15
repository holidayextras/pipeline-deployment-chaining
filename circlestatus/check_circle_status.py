import requests
import sys
import time
import logging

# create logger
logger = logging.getLogger('circle status')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s '
                              '- %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

# Pass in circleci environment variable from a pipeline repo
circle_link = sys.argv[1]
response_limit = '1'

logger.debug('starting')


def circle_request():
    json_attempts = 10

    try:
        while json_attempts > 0:
            r = requests.get('{}&limit={}'.format(circle_link, response_limit))
            if r.status_code != 200:
                json_attempts -= 1
            else:
                break
    except AttributeError:
        logger.error('failed to get link')
    return r.json()[0]


def circle_status():
    poll_tries = 0
    build = circle_request()

    while poll_tries > 0:
        if build['lifecycle'] == 'running' and build['outcome'] is None:
            time.sleep(10)
            poll_tries -= 1
            build = circle_request()
        else:
            return 'kicking off pipeline controller'

    if poll_tries == 0:
        # TODO write to stderr easier to spot red content in circleci
        logging.warning('Ran out of tries!')
        sys.exit(1)

if __name__ == '__main__':
    circle_status()
