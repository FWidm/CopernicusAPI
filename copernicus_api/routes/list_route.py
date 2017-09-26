from flask import Blueprint, jsonify, app

from copernicus_api import misc
from copernicus_api.misc.file_status import file_status

list_route = Blueprint('list', __name__)
@list_route.route('/list')
def list():
    return misc.create_response(jsonify({'files':file_status.get_available_files()}))
