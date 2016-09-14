import requests
import sys
import time

# Pass in circleci environment variable from a pipeline repo
github_organisation = sys.argv[1] # GITHUB_ORG
repository = sys.argv[2] # NEXT_PROJECT
circle_token = sys.argv[3] # CIRCLE_TOKEN
response_limit = '1'


def circle_request():
    json_attempts = 10

    while json_attempts > 0:
        r = requests.get('https://circleci.com/api/v1.1/project/github/{}/{}/tree/dependency-graph?circle-token={}&limit={}'.format(
            github_organisation,
            repository,
            circle_token,
            response_limit)
        )
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
        # TODO consider writing to stderr for easier to spot red content in circleci
        print('Ran out of time!')
        exit(1)

if __name__ == '__main__':
    circle_status()
