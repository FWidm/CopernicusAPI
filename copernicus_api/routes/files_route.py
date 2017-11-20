from flask import Blueprint, jsonify, app

from copernicus_api import misc
from copernicus_api.actions.list_files_action import list_files
from copernicus_api.misc.file_status import file_status
from copernicus_api.schemas.message_schema import MessageSchema

files_route = Blueprint('files', __name__)
@files_route.route('/files')
def list():
    # return misc.create_response(jsonify({'files':list_files()}))
    result = list_files()
    #transform
    msg = {'message': "All currently available files.", 'data': result}
    schema = MessageSchema()
    result = schema.dump(msg)

    return misc.create_response(jsonify(result.data))
