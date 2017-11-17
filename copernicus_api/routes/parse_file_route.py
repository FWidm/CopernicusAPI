import json
import os

import dateutil.parser
from copernicus_retrieval.data.copernicus_data import CopernicusData
from flask import Blueprint, jsonify, request, Response

from copernicus_api import misc
from copernicus_api.actions import parse_action, check_regex_action
from copernicus_api.misc import cache
from copernicus_api.misc.settings import file_directory
from copernicus_api.misc.file_status import file_status

parse_file_route = Blueprint('parse', __name__)


@parse_file_route.route('/parse', methods=['GET'])
def parse_file_():
    """
    Retrieves the parsed information  by specifying the file, the timestamp and latitude + longitude. Don't forget
    to encode the plus sign '+' = %2B!
    Example: GET /parse/data/ecmwf/an-2017-09-14.grib?timestamp=2017-09-16T15:21:20%2B00:00&lat=48.398400&lon=9.591550
    :param fileName: path to a retrieved ecmwf grib file.
    :return: OK including json content or empty not found
    """
    try:
        [point, date] = validate_request_parameters()
    except ValueError, e:
        return misc.create_response(jsonify(message=e.message), 400)

    file_name = misc.build_file_name(date)
    path_to_file = file_directory + os.sep + file_name
    files = file_status.get_available_files()

    if file_name not in files or not os.path.isfile(path_to_file):
        return misc.create_response(jsonify({
            'message': 'Given filename={} could not be found in the available files are attached.'.format(file_name, files),
            'available_files': files}), 404)

    response = cache.cache.get(request.url)
    # check cache
    if response:  # got cache result
        return Response(json.dumps(response, default=CopernicusData.json_serial, indent=2), mimetype="text/json",
                        status=200)

    return parse_action.parse(path_to_file, point, date)


@parse_file_route.route('/parse/<path:file_name>', methods=['GET'])
def parse_file(file_name):
    """
    Retrieves the parsed information  by specifying the file, the timestamp and latitude + longitude. Don't forget
    to encode the plus sign '+' = %2B!
    Example: GET /parse/data/ecmwf/an-2017-09-14.grib?timestamp=2017-09-16T15:21:20%2B00:00&lat=48.398400&lon=9.591550
    :param fileName: path to a retrieved ecmwf grib file.
    :return: OK including json content or empty not found
    """
    path_to_file = file_directory + os.sep + file_name
    try:
        [point, date] = validate_request_parameters()
    except ValueError, e:
        return misc.create_response(jsonify(message=e.message), 400)

    files = file_status.get_available_files()
    if file_name not in files or not os.path.isfile(path_to_file):
        return misc.create_response(jsonify({
            'message': 'Given filename={} could not be found in the available files list={}'.format(file_name, files),
            'available_files': files}), 404)

    response = cache.cache.get(request.url)
    # check cache
    if response:  # got cache result
        return Response(json.dumps(response, default=CopernicusData.json_serial, indent=2), mimetype="text/json",
                        status=200)

    return parse_action.parse(path_to_file, point, date)


def validate_request_parameters():
    """
    Checks the expected params lat, lon and timestamp and makes sure that the values are inside the specified parameters.
    :param file_name: filename that was given via url params
    :param path_to_file: constructed path to the file
    :return: an array consisting of a point [lat,lon] and the timestamp
    """
    timestamp = request.args.get('timestamp')
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        raise ValueError(
            "Latitude or Longitude are not inside their bounds. Lat is expected to be in [-90,90] and lon inside of [-180,180]. Received values: [{lat},{lon}]".format(
                lat=lat, lon=lon))
    point = [lat, lon]

    if timestamp is None or timestamp == "" or not check_regex_action.check_iso_string(timestamp):
        raise ValueError(
            "Timestamp query parameter is required. Please provide it like this: /retrieve?timestamp=2017-09-14T15:21:20%2B00:00. Received string={}".format(
                timestamp))

    return [point, dateutil.parser.parse(timestamp).replace(tzinfo=None)]
