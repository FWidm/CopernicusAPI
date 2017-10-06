import argparse
import os

import errno

from copernicus_api.misc.settings import file_directory


def build_file_name(date):
    """
    Builds the resulting grib file by appending the date in isoformat to the prefix and adding the file suffix afterwards
    :param date: requested date
    :return: filename string
    """
    return settings.file_prefix + date.date().isoformat() + settings.__file_suffix


def create_response(json, code=200):
    """
    Create a json response with a custom HTTP code.
    :param json: result of jsonify
    :param code: responsecode, 200 is the default one
    :return: Response to the callee
    """
    response = json
    response.status_code = code
    response.mimetype = "text/json"
    return response


def get_cli_arguments():
    """
    Parses the 6 required parameters "directory" that specifies the storage directory, "host", "port", "threaded":bool, "debug":bool, "timeout": for caches in seconds.
    :return: parsed arguments
    """
    parser = argparse.ArgumentParser("flask_sample.py")
    parser.add_argument("directory", help="Storage directory of the copernicus data", type=str)
    parser.add_argument("host", help="Host", type=str)
    parser.add_argument("port", help="Port this flask app shall use", type=int)
    parser.add_argument("threaded", help="Should the flask instance run threaded or not", type=bool)
    parser.add_argument("debug", help="Should the flask instance run in debug mode or not", type=bool)
    parser.add_argument("timeout", help="Cache timeout in seconds", type=int, default=60 * 60)
    return parser.parse_args()


def make_directories(directory_path):
    """
    Recursively create required directories if they do not exist.
    :param directory_path: path/to/directory
    """
    try:
        os.makedirs(directory_path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(directory_path):
            pass
        else:
            raise
