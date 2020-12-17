import argparse
from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask_restful import Api
from api.common.logging import configure_logging
from api.common.structure import configuration_path
from api.common.utilities import ensure_structure, measure_runtime
from api.configuration.configuration import APIConfiguration
from api.dsp.externals.validations import validate_features_availability
from api.resources.featurizer import FeaturizerResource


# Initialize the flask application and the API
app = Flask(__name__)
api = Api(app)

# Configure the logging
configure_logging()

# Load the API-level configuration
api_configuration = APIConfiguration(configuration_path).load()

# load up the .env configuration entries as environment variables
load_dotenv(find_dotenv())

# Ensure the presence of the directories excluded from the version control (logging files directory)
ensure_structure(logs_dir=True)

# Prepare the featurizer resource supported by the API
api.add_resource(FeaturizerResource, "/featurize")


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
    if validate_features_availability():
        app.run(host=host_, port=port_, debug=args.debug)
