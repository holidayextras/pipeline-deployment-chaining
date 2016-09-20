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
    try:
        while json_attempts > 0:
            r = requests.get('{}&limit={}'.format(circle_link, response_limit))
            if r.status_code != 200:
                json_attempts -= 1
            else:
                r = r.json()[0]
                if r['outcome'] and r['lifecycle']:
                    break
                json_attempts -= 1
    except Exception as e:
        logger.error({'error': e})
    return r


def circle_status():
    poll_tries = config_poll_tries
    build = circle_request()

    while poll_tries > 0:
        try:
            if build['lifecycle'] == 'running' and build['outcome'] is None:
                time.sleep(sleep_time)
                poll_tries -= 1
                build = circle_request()
            else:
                print("Success")
                return True
        except Exception as e1:
            logger.error({"error": e1})
            break

    if poll_tries == 0:
        logger.warning('Ran out of tries!')

if __name__ == '__main__':
    circle_status()
