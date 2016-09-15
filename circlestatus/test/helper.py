import json
import os
from pip.commands import help

WORKING_DIR = os.path.abspath(os.path.dirname(__file__))
HAPI_RESPONSES_DIR = WORKING_DIR + '/path/to/dir'

def load_json_from_file(basename):

    with open(basename) as fin:
        input_json = json.load(fin)

    return input_json
