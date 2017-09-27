import os

import sys
from copernicus_retrieval import retrieve
from copernicus_retrieval.data import copernicus_enums
from flask import request, jsonify
from socket import error as socket_error

from copernicus_api import misc
from copernicus_api.misc import directory, settings
from copernicus_api.misc import cache
from copernicus_api.misc.file_status import file_status


def retrieve_file(date_arg):
    """
    Retrieves the file if it is not in our file_status object or if it's marked as available (as the library also checks if the file exists locally)
    :param date_arg: iso timestamp string
    :return:  Response object with either the filename or a message
    """
    file_name = misc.build_file_name(date_arg)
    path_to_file = directory + os.sep + file_name

    # first call only: check if the file exists, if not we can download
    if not file_status.in_files(file_name) or file_status.is_available(file_name):
        # todo: this should be pushed into a queue to make the call nonblocking. Or make the call return "accepted" and let the client use list until the file is available.
        # mark file as in progress by adding it to the files.
        file_status.add_file(file_name)
        # retrieve
        r = retrieve.Retrieve()
        try:
            result = r.retrieve_file(path_to_file, date=date_arg,
                                     data_type=copernicus_enums.DataType.ANALYSIS,filter_europe=True)
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
        except socket_error, e:
            file_status.remove_file(file_name)
            return misc.create_response(jsonify({'message': "Socket Error: {} - {} ".format(e.errno, e.strerror)}))
    # is matched if the file is in our file list, but not retrieved
    elif not file_status.is_available(file_name):
        return misc.create_response(jsonify({
            'message': 'Download is currently in progress. Retry this operation to retrieve the filename in a minute.'}),
            202)