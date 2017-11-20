from flask import Blueprint, jsonify

from copernicus_api import misc
from copernicus_api.schemas.message_schema import MessageSchema

index_route = Blueprint('index', __name__)
@index_route.route('/')
def hello_world():
    """
    Heartbeat
    :return:
    """
    msg = {'message': "Hello Copernicus."}
    schema = MessageSchema()
    return misc.create_response(jsonify(schema.dump(msg).data))
