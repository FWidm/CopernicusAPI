from datetime import datetime, timedelta
import dateutil
import os
from copernicus_retrieval import retrieve
from copernicus_retrieval.data import copernicus_enums
from flask import Blueprint, jsonify, request
import dateutil.parser

from copernicus_api import misc
from copernicus_api.misc import cache
from copernicus_api.misc.settings import directory
from copernicus_api.misc.file_status import file_status

retrieve_file_route = Blueprint('retrieve_file', __name__)


@retrieve_file_route.route('/retrieve', methods=['GET'])
def retrieve_copernicus_file():
    """
    Retrieve the grib file for a given date.
    Example query: /retrieve?timestamp=2017-09-13T15:21:20%2B00:00
    # :return: filename    """
    timestamp = request.args.get('timestamp')
    if timestamp is None or timestamp == "" or not misc.check_date_string_format(timestamp):
        response = misc.create_response(jsonify(
            message="Timestamp query parameter is required. Please provide it like this: ?timestamp=2017-09-14T15:21:20%2B00:00"),
            404)
        return response
    date_arg = dateutil.parser.parse(timestamp).replace(tzinfo=None)
    print "date={}".format(date_arg)
    response = cache.cache.get(request.url.split("T")[0])
    # check cache hit
    if response:
        return jsonify(fileName=response)

    # no cache hit
    latestRetrievalDate = datetime.utcnow() - timedelta(days=copernicus_enums.DataSets.CAMS.value['delayDays'])
    if ((date_arg - latestRetrievalDate).days <= 0):
        return retrieve_file(date_arg)
    else:
        return misc.create_response(jsonify(
            message="Cannot retrieve files for this date. Latest retrieval date is {}".format(
                latestRetrievalDate.isoformat())))

def retrieve_file(date_arg):
    """
    Retrieves the file if it is not in our file_status object or if it's marked as available (as the library also checks if the file exists locally)
    :param date_arg: iso timestamp string
    :return:  Response object with either the filename or a message
    """
    dateString = date_arg.strftime(retrieve.Retrieve.DATEFORMAT)

    file_name = "an-" + dateString + ".grib"
    path_to_file = directory + os.sep + file_name

    # first call only: check if the file exists, if not we can download
    if not file_status.in_files(file_name) or file_status.is_available(file_name):
        # todo: this should be pushed into a queue to make the call nonblocking. Or make the call return "accepted" and let the client use list until the file is available.
        # mark file as in progress by adding it to the files.
        file_status.add_file(file_name)
        # retrieve
        r = retrieve.Retrieve()
        result = r.retrieve_file(path_to_file, date=date_arg,
                                 data_type=copernicus_enums.DataType.ANALYSIS)
        print "Download complete"
        if result is not "":
            # set the cache for the exact query, we might want to filter the hours from the given timestamp so that it matches 2017-09-19T* for example.
            cache.cache.set(request.url.split("T")[0], result, timeout=cache.retrieve_timeout)
            # mark the file as retrieved
            file_status.mark_available(file_name, directory)
            return misc.create_response(jsonify({'file_name':result.split("/")[-1]}))
        else:
            # should not happen - will notify you if r.retrieve will not return anything.
            return misc.create_response(jsonify({
                'message': 'An unexpected error occured - the requested file could not bre retrieved from the ECMWF server'}),
                503)
    # is matched if the file is in our file list, but not retrieved
    elif not file_status.is_available(file_name):
        return misc.create_response(jsonify({
            'message': 'Download is currently in progress. Retry this operation to retrieve the filename in a minute.'}),
            202)
