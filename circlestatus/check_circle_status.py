import requests
import sys
import time
import tools

config_json_attempts, config_poll_tries, sleep_time, response_limit \
    = tools.get_config_variables()

logger = tools.init_a_logger()
# Pass in circleci environment variable from a pipeline repo
circle_link = sys.argv[1]


def circle_request():
    r = ''
    json_attempts = config_json_attempts

    while json_attempts > 0:
        r = requests.get('{}&limit={}'.format(circle_link, response_limit))
        if r.status_code != 200:
            json_attempts -= 1
        else:
            r = r.json()[0]
            break
    return r


def circle_status():
    poll_tries = config_poll_tries
    try:
        build = circle_request()
    except Exception as e1:
        logger.error({'error': e1})
        sys.exit(1)

    while poll_tries > 0:
        if build['lifecycle'] == 'running' and build['outcome'] is None:
            time.sleep(sleep_time)
            poll_tries -= 1
            build = circle_request()
        else:
            break

    if poll_tries == 0:
        logger.warning('Ran out of tries!')
        sys.exit(1)


def main():
    try:
        circle_status()
        logger.debug('completed circle poll')
    except Exception as e2:
        logger.error({'error': e2})
        sys.exit(1)
    logger.debug('posting to circle')
    requests.post(circle_link)

if __name__ == '__main__':
    main()
