import argparse
import os
import re

from copernicus_api.misc.settings import directory


def init_folder_structure():
    if not os.path.exists(directory):
        os.makedirs(directory)


def check_date_string_format(timestamp):
    """
    Checks if the timestamp matches the ISO Date format. Source for the regex: https://stackoverflow.com/a/6709493/1496040
    :param timestamp: string timestamp
    :return: true if it matches the iso format | false if not
    """
    RegEx = re.compile(r'^\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$')
    return bool(RegEx.search(timestamp))


def create_response(json, code=200):
    """
    Create a json response with a custom HTTP code.
    :param json: result of jsonify
    :param code: responsecode, 200 is the default one
    :return: Response to the callee
    """
    response = json
    response.status_code = code
    return response


def get_local_files(directory):
    files = [f for f in os.listdir(directory) if
             os.path.isfile(directory + os.sep + f) and not f.startswith(".") and f.endswith(".grib")]
    print files
    return files


def get_cli_arguments():
    parser = argparse.ArgumentParser("flask_sample.py")
    parser.add_argument("directory", help="Storage directory of the copernicus data", type=str)
    parser.add_argument("host", help="Host", type=str)
    parser.add_argument("port", help="Port this flask app shall use", type=int)
    parser.add_argument("threaded", help="Should the flask instance run threaded or not", type=bool)
    parser.add_argument("debug", help="Should the flask instance run in debug mode or not", type=bool)
    parser.add_argument("timeout", help="Cache timeout in seconds", type=int, default=60 * 60)
    return parser.parse_args()