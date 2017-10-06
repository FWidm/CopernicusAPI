import logging
from logging.handlers import RotatingFileHandler

from os import sep
from flask import Flask
from copernicus_api import misc
from copernicus_api.misc import settings
from copernicus_api.routes.parse_file_route import parse_file_route
from copernicus_api.routes.index_route import index_route
from copernicus_api.routes.list_route import list_route
from copernicus_api.routes.retrieve_file_route import retrieve_file_route

app = Flask(__name__)


# Blueprints
app.register_blueprint(index_route)
app.register_blueprint(list_route)
app.register_blueprint(retrieve_file_route)
app.register_blueprint(parse_file_route)


if __name__ == '__main__':
    args = misc.get_cli_arguments()
    misc.file_directory = args.directory
    timeout = args.timeout
    misc.make_directories(settings.logging_directory)
    misc.make_directories(settings.file_directory)

    formatter = logging.Formatter(settings.log_format,datefmt=settings.date_format)

    handler = RotatingFileHandler(settings.logging_directory+sep+'copernicus_api.log', maxBytes=10000, backupCount=1)
    handler.setFormatter(formatter)

    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    # print(app.config["files"])
    app.run(host=args.host, port=args.port, debug=args.debug, threaded=args.threaded)
