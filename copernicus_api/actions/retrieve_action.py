import os

import sys
from time import sleep

from copernicus_retrieval import retrieve
from copernicus_retrieval.data import copernicus_enums
from flask import request, jsonify
from socket import error as socket_error

from copernicus_api import misc
from copernicus_api.misc import file_directory, settings
from copernicus_api.misc import cache
from copernicus_api.misc.executor import executor
from copernicus_api.misc.file_status import file_status
from flask import current_app


def download_action(path_to_file, date_arg, data_type, filter_europe):
    """
    action to be called within another thread
    :param path_to_file: path to the downloaded file
    :param date_arg: date of retrieval
    :param data_type: where is the data stored
    :param filter_europe: do we want only european files?
    :return: Filename if successful, None if an error occurs.
    """
    file_name = path_to_file.split("/")[-1]
    try:
        r = retrieve.Retrieve()
        result = r.retrieve_file(path_to_file, date=date_arg,
                                 data_type=data_type, filter_europe=filter_europe)
        # mark the file as retrieved
        file_status.mark_available(result.split("/")[-1], file_directory)
    except (socket_error, RuntimeError) as e:
        file_status.remove_file(file_name)
        return None
    return result


def retrieve_file(date_arg):
    """
    Retrieves the file if it is not in our file_status object or if it's marked as available (as the library also checks if the file exists locally)
    :param date_arg: iso timestamp string
    :return:  Response object with either the filename or a message
    """
    file_name = misc.build_file_name(date_arg)
    path_to_file = file_directory + os.sep + file_name
    current_app.logger.info("{} in files: {}? {}".format(file_name, file_status.get_available_files(), file_status.in_files(file_name)))
    current_app.logger.info("{} is available? {}".format(file_name, file_status.is_available(file_name)))

    # first call only: check if the file exists, if not we can download
    if file_status.is_available(file_name):
        cache.cache.set(request.url.split("T")[0], file_name, timeout=cache.retrieve_timeout)
        return {'message': 'File is available.', 'data': {'file_name': file_name.split("/")[-1]}}
    # file is not available AND not in files (in progress)
    elif not file_status.in_files(file_name):
        # mark file as in progress by adding it to the files.
        file_status.add_file(file_name)
        # retrieve via executor
        future = executor.submit(download_action, path_to_file, date_arg, copernicus_enums.DataType.ANALYSIS, True)
        # todo: check if this query works as expected - we either receive the future's results or can surpass it if the file is available
        current_app.logger.info(file_status.is_available(file_name))
        if future.done() or file_status.is_available(file_name):
            # set the cache for the exact query, we might want to filter the hours from the given timestamp so that it matches 2017-09-19T* for example.
            cache.cache.set(request.url.split("T")[0], future.result(), timeout=cache.retrieve_timeout)
            return {'message':'File is available.','data': {'file_name':file_name.split("/")[-1]}}
    # default response will be the download message
    return {'message': 'Download is currently in progress. Retry this operation to retrieve the filename in a minute.'}
