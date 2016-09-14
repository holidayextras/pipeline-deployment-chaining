import os
from helper import load_json_from_file

WORKING_DIR = os.path.abspath(os.path.dirname(__file__))
SOME_DIR = WORKING_DIR + '/path/to/dir'

sample_circle_response = load_json_from_file(WORKING_DIR + '/circle_response.json')