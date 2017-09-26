import json
import os
from copernicus_retrieval import parser as copernicus_parser
from copernicus_retrieval.data import copernicus_enums
from copernicus_retrieval.data.copernicus_data import CopernicusData
from flask import Blueprint, jsonify, request, Response

from copernicus_api import misc
from copernicus_api.misc import cache
from copernicus_api.misc.settings import directory
from copernicus_api.misc.file_status import file_status

parse_file_route = Blueprint('parse', __name__)
@parse_file_route.route('/parse/<path:fileName>', methods=['GET'])
def parse_file(fileName):
    """
    Retrieves the parsed information  by specifying the file, the timestamp and latitude + longitude. Don't forget
    to encode the plus sign '+' = %2B!
    Example: GET /parse/data/ecmwf/an-2017-09-14.grib?timestamp=2017-09-16T15:21:20%2B00:00&lat=48.398400&lon=9.591550
    :param fileName: path to a retrieved ecmwf grib file.
    :return: OK including json content or empty not found
    """
    timestamp = request.args.get('timestamp')
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    pathToFile = directory + os.sep + fileName
    files = file_status.get_available_files()

    if fileName not in files or not os.path.isfile(pathToFile):
        response = misc.create_response(jsonify(
            message="Given filename={} could not be found in the available files list={}".format(fileName, files)),
            404)
        return response

    if timestamp is None or timestamp == "" or not misc.check_date_string_format(timestamp):
        response = misc.create_response(jsonify(
            message="Timestamp query parameter is required. Please provide it like this: /retrieve?timestamp=2017-09-14T15:21:20%2B00:00"),
            404)
        return response

    if lon is None or lon is "" or lat is None or lat is "":
        response = misc.create_response(jsonify(
            message="Latitude or Longitude is required. Please specify both values like this: lat=48.398400&lon=9.591550"),
            404)
        return response

    point = [float(lat), float(lon)]
    print point

    queriedTimes = copernicus_enums.Time.convert_timestamp_to_times(timestamp)
    response = cache.cache.get(request.url)
    # check cache
    if response is None:
        parser = copernicus_parser.Parser()
        result = parser.get_nearest_values(pathToFile, point, parameters=copernicus_enums.ParameterCAMS.all(),
                                           times=queriedTimes)
        cache.cache.set(request.url, result, cache.timeout)
        return Response(json.dumps(result, default=CopernicusData.json_serial, indent=2), mimetype="text/json",
                        status=200)

    else:  # got cache result
        return Response(json.dumps(response, default=CopernicusData.json_serial, indent=2), mimetype="text/json",
                        status=200)
