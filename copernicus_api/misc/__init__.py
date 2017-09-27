import argparse
import os

from copernicus_api.misc.settings import directory


def init_folder_structure():
    if not os.path.exists(directory):
        os.makedirs(directory)


def  build_file_name(date):
    return settings.file_prefix+date.date().isoformat()+settings.__file_suffix


def create_response(json, code=200):
    """
    Create a json response with a custom HTTP code.
    :param json: result of jsonify
    :param code: responsecode, 200 is the default one
    :return: Response to the callee
    """
    response = json
    response.status_code = code
    response.mimetype="text/json"
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