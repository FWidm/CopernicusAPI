from datetime import datetime, timedelta
import dateutil
from copernicus_retrieval.data import copernicus_enums
from flask import Blueprint, jsonify, request
import dateutil.parser

from copernicus_api import misc
from copernicus_api.actions import retrieve_action
from copernicus_api.misc import cache


retrieve_file_route = Blueprint('retrieve_file', __name__)


@retrieve_file_route.route('/retrieve', methods=['GET'])
def retrieve_copernicus_file():
    """
    Retrieve the grib file for a given date.
    Example query: /retrieve?timestamp=2017-09-13T15:21:20%2B00:00
    # :return: filename    """

    try:
        date_arg = validate_request_parameters()

    except ValueError, e:
        return misc.create_response(jsonify(message=e.message), 400)

    response = cache.cache.get(request.url.split("T")[0])

    # check cache hit
    if response:
        return misc.create_response(jsonify({'file_name': response.split("/")[-1]}))

    # no cache hit
    latestRetrievalDate = datetime.utcnow() - timedelta(days=copernicus_enums.DataSets.CAMS.value['delayDays'])
    if ((date_arg - latestRetrievalDate).days <= 0):
        return retrieve_action.retrieve_file(date_arg)
    else:
        return misc.create_response(jsonify(
            message="Cannot retrieve files for this date. Latest retrieval date is {}".format(
                latestRetrievalDate.isoformat())))


def validate_request_parameters():
    """
    Validate the given timestamp request param
    :return: dumb datetime object
    """
    timestamp = request.args.get('timestamp')
    if timestamp is None or timestamp == "" or not misc.check_date_string_format(timestamp):
        raise ValueError("Timestamp query parameter is required. Please provide it like this: ?timestamp=2017-09-14T15:21:20%2B00:00. Received string={}".format(timestamp))
    return dateutil.parser.parse(timestamp).replace(tzinfo=None)