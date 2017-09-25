from datetime import datetime, timedelta
import dateutil
import os
from copernicus_retrieval import retrieve
from copernicus_retrieval.data import copernicus_enums
from flask import Blueprint, jsonify, request, Response
import dateutil.parser

from copernicus_api import misc
from copernicus_api.misc import cache
from copernicus_api.misc.settings import directory


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
    date = dateutil.parser.parse(timestamp).replace(tzinfo=None)
    print "date={}".format(date)
    response = cache.cache.get(request.url)
    if response is None:
        r = retrieve.Retrieve()
        latestRetrievalDate = datetime.utcnow() - timedelta(days=copernicus_enums.DataSets.CAMS.value['delayDays'])
        diff = date - latestRetrievalDate
        print "days={}".format(diff.days)
        result = ""
        if (diff.days <= 0):
            dateString = date.strftime(retrieve.Retrieve.DATEFORMAT)
            print "retrievalDate={}; type={}".format(dateString, type(dateString))
            # todo: this should be pushed into a queue to make the call nonblocking. Or make the call return "accepted" and let the client use list until the file is available.
            pathToFile = directory + os.sep + "an-" + dateString

            result = r.retrieve_file(pathToFile, date=latestRetrievalDate, data_type=copernicus_enums.DataType.ANALYSIS)
            files = misc.get_local_files(directory)
            print "Writing completed!"
            cache.cache.set(request.url, result, cache.timeout)
            return jsonify(fileName=result.split("/")[-1])

        else:
            return misc.create_response(jsonify(
                message="Cannot retrieve files for this date. Latest retrieval date is {}".format(
                    latestRetrievalDate.isoformat())))
    else:
        return jsonify(fileName=response.split("/")[-1])

