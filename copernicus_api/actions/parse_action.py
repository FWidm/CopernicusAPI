import json
import os
from copernicus_retrieval import parser as copernicus_parser
from copernicus_retrieval.data import copernicus_enums
from copernicus_retrieval.data.copernicus_data import CopernicusData
from flask import request, Response

from copernicus_api.misc import cache


def parse(path_to_file, point, date):
    """
    Uses the given parameters to retrieve the requested data from the dataset
    :param path_to_file: path to the file
    :param point: geo coordinates in the form [lat:float, lon:float]
    :param timestamp:  iso timestamp
    :return: reponse
    """
    queriedTimes = copernicus_enums.Time.convert_date_to_times(date)

    parser = copernicus_parser.Parser()
    result = parser.get_nearest_values(path_to_file, point, parameters=copernicus_enums.ParameterCAMS.all(),
                                       times=queriedTimes)
    # put the result in the cache with the normal timeout
    cache.cache.set(request.url, result, cache.timeout)
    return Response(json.dumps(result, default=CopernicusData.json_serial, indent=2), mimetype="text/json",
                    status=200)
