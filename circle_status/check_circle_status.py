import requests
import sys
import time
import logging

logger = logging.basicConfig(level=logging.INFO)

# Pass in circleci environment variable from a pipeline repo
circle_link = sys.argv[1]
response_limit = '1'

logging.debug('starting')


def circle_request():
    json_attempts = 10

    while json_attempts > 0:
        r = requests.get('{}&limit={}'.format(circle_link, response_limit))
        if r.status_code != 200:
            json_attempts -= 1
        else:
            break
    return r.json()[0]


def circle_status():
    poll_tries = 60
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
