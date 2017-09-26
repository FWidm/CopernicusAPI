from flask import Flask
from copernicus_api import misc
from copernicus_api.misc.file_status import file_status
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
    misc.directory = args.directory
    misc.init_folder_structure()
    timeout = args.timeout

    # print(app.config["files"])
    app.run(host=args.host, port=args.port, debug=args.debug, threaded=args.threaded)
