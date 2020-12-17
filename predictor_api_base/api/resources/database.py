from flask_restful import Resource, reqparse, abort
from api.common.logging import get_logger
from api.database.entities import PredictorModelEntity
from api.database.managers import PredictorModelManager


# Create the module-level predictor model resource logger
logger = get_logger("PredictorModelResource", propagate=True)


class PredictorModelResource(Resource):
    """Class implementing the predictor model creator API resource"""

    # Request arguments parser
    parser = reqparse.RequestParser()

    # Supported request arguments
    parser.add_argument("model", type=str, help="String with the model settings (configuration)")

    # Predictor model manager
    manager = PredictorModelManager()

    @staticmethod
    def abort_due_to_existing_model(args):
        """
        Abort due to already existing model configuration in the database.
        :param args: requests arguments.
        :type args: reqparse.Argument.
        :return: None.
        """
        abort(f"401", message=f"Model {args} already exists, update it if needed")

    @staticmethod
    def abort_due_to_non_existing_model(args):
        """
        Abort due to non existence of the model configuration in the database.
        :param args: requests arguments.
        :type args: reqparse.Argument.
        :return: None.
        """
        abort(f"402", message=f"Model {args} does not exist, create it if needed")

    @staticmethod
    def abort_due_to_model_manager_failed(args, e):
        """
        Abort due to model manager failed.
        :param args: requests arguments.
        :type args: reqparse.Argument.
        :param e: Exception alias.
        :type e: Exception.
        :return: None.
        """
        logger.exception(e)
        abort(f"403", message=f"Model manager (args: {args}) failed")

    def raise_for_existing_model(self, model_entity, args):
        """
        Raise for the existing model case.
        :param model_entity: model entity.
        :type model_entity: PredictorModelEntity instance.
        :param args: requests arguments.
        :type args: reqparse.Argument.
        :return: None.
        """
        if self.get_model(model_entity, args):
            self.abort_due_to_existing_model(args)

    def raise_for_non_existing_model(self, model_entity, args):
        """
        Raise for the existing model case.
        :param model_entity: model entity.
        :type model_entity: PredictorModelEntity instance.
        :param args: requests arguments.
        :type args: reqparse.Argument.
        :return: None.
        """
        if not self.get_model(model_entity, args):
            self.abort_due_to_non_existing_model(args)

    def get_model(self, model_entity, args):
        """
        Gets the model record using its model entity and the input arguments.
        :param model_entity: model entity.
        :type model_entity: PredictorModelEntity instance.
        :param args: requests arguments.
        :type args: reqparse.Argument.
        :return: model record.
        """
        try:
            return self.model_manager.get(model_name=model_entity["name"])
        except Exception as e:
            self.abort_due_to_model_manager_failed(args, e)

    def set_model(self, model_entity, args):
        """
        Sets the model record using its model entity and the input arguments.
        :param model_entity: model entity.
        :type model_entity: PredictorModelEntity instance.
        :param args: requests arguments.
        :type args: reqparse.Argument.
        :return: stored model record uid.
        """
        try:
            return self.model_manager.set(data=model_entity)
        except Exception as e:
            self.abort_due_to_model_manager_failed(args, e)

    def post(self):
        """
        Handles the HTTP POST request to create a new predictor model settings (configuration) record
        in the database. In case a model configuration for the requested model name already exists,
        the call is aborted.
        :return: dict with the created record id and additional meta information.
        """

        # Parse the HTTP POST requests arguments (strict settings: all args must be specified)
        args = self.parser.parse_args(strict=True)

        # Get the predictor model entity from the parsed model
        model_entity = PredictorModelEntity.from_json(args["model"])

        # Handle the existing model record
        self.raise_for_existing_model(model_entity, args)

        # Create the predictor model record (<uid> is a str (id of the created record))
        uid = self.set_model(model_entity, args)

        # Return the response
        return {
            "id": uid,
            "model": args["model"]
        }

    def put(self):
        """
        Handles the HTTP PUT request to update an existing predictor model settings (configuration)
        record in the database. In case a model configuration for the requested model name does not
        exist, the call is aborted.
        :return: dict with the updated record id(s) and additional meta information.
        """

        # Parse the HTTP PUT requests arguments (strict settings: all args must be specified)
        args = self.parser.parse_args(strict=True)

        # Get the predictor model entity from the parsed model
        model_entity = PredictorModelEntity.from_json(args["model"])

        # Handle the non-existing model record
        self.raise_for_non_existing_model(model_entity, args)

        # Update the predictor model record (<uid> is a list (ids of the updated records))
        uid = self.set_model(model_entity, args)

        # Return the response
        return {
            "id": uid,
            "model": args["model"]
        }

    def get(self):
        """
        Handles the HTTP Get request to obtain an existing predictor model settings (configuration)
        record from the database. In case a model configuration for the requested model name does
        not exist, the call is aborted.
        :return: dict with the obtained record and additional meta information.
        """

        # Parse the HTTP GET requests arguments (strict settings: all args must be specified)
        args = self.parser.parse_args(strict=True)

        # Get the predictor model
        #
        #  1. Get the predictor model entity from the parsed model
        #  2. Get the predictor model record
        model_entity = PredictorModelEntity.from_json(args["model"])
        model_record = self.get_model(model_entity, args)

        # Handle the non-existing model record
        self.raise_for_non_existing_model(model_entity, args)

        # Return the response
        return {
            "record": model_record.as_json,
            "model": args["model"]
        }
