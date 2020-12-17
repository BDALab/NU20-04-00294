import argparse
from flask import Flask
from flask_restful import Api
from api.common.logging import configure_logging
from api.common.structure import configuration_path
from api.common.utilities import ensure_structure, measure_runtime
from api.configuration.configuration import APIConfiguration
from api.resources.predictor import PredictorResource
from api.resources.database import PredictorModelResource


# Initialize the flask application and the API
app = Flask(__name__)
api = Api(app)

# Configure the logging
configure_logging()

# Load the API-level configuration
api_configuration = APIConfiguration(configuration_path).load()

# Ensure the presence of the directories excluded from the version control
#
#  1. database directory
#  2. ml models directory
#  3. logging files directory
ensure_structure(database_dir=True, models_dir=True, logs_dir=True)

# Prepare the resources supported by the API
#
#  1. predictor resource
#  2. predictor model resources
api.add_resource(PredictorResource, "/predict", "/predict/<features>")
api.add_resource(PredictorModelResource, "/model", "/model/<model>")


@measure_runtime
def main(host, port, debug=False):
    """
    Runs the API.
    :param host: hostname or ip address to listen on.
    :type host: str.
    :param port: port of the web-server.
    :type port: int.
    :param debug: debug mode.
    :type debug: bool.
    :return: None.
    """
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":

    # Prepare the command line arguments
    parser = argparse.ArgumentParser(description="API")
    parser.add_argument("--host", help="the hostname to listen on (defaults to '127.0.0.1')", type=str)
    parser.add_argument("--port", help="the port of the web-server (defaults to 5000)", type=int)
    parser.add_argument("--debug", help="debug run", action="store_true")

    # Parse the command line arguments
    args = parser.parse_args()

    # Prepare the default args
    host_ = args.host if args.host else "127.0.0.1"
    port_ = args.port if args.port else 5000

    # Run the API
    main(host_, port_, debug=args.debug)
