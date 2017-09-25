from flask import Blueprint, jsonify, app

list_route = Blueprint('list', __name__)
@list_route.route('/list')
def list():
    return "hello!"
