from flask import Blueprint, jsonify

from copernicus_api import misc

index_route = Blueprint('index', __name__)
@index_route.route('/')
def hello_world():
    """
    Heartbeat
    :return:
    """
    return misc.create_response(jsonify("Hello ECMWF API!"))
