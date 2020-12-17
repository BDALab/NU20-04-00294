from flask_restful import Resource, reqparse, abort
from api.common.logging import get_logger
from api.ml.utilities.inputs import Features
from api.ml.utilities.outputs import Predictions
from api.ml.preprocessors.features_preprocessors import FeaturesPreprocessor
from api.ml.predictors.predictor import PredictorLoader, NoLoadablePredictorException
from api.database.entities import PredictorModelEntity
from api.database.managers import PredictorModelManager


# Create the module-level predictor resource logger
logger = get_logger("PredictorResource", propagate=True)


class PredictorResource(Resource):
    """Class implementing the predictor API resource"""

    # Request arguments parser
    parser = reqparse.RequestParser()

    # Supported request arguments
    parser.add_argument("features", type=str, help="Dict with the features")
    parser.add_argument("model", type=str, help="String with the predictor model name")

    # Predictor model manager
    model_manager = PredictorModelManager()

    @staticmethod
    def abort_due_to_incomplete_args(args):
        """
        Abort due to incomplete requests arguments.
        :param args: requests arguments.
        :type args: reqparse.Argument.
        :return: None.
        """
        abort(f"401", message=f"Request args {args} (features and model must be provided)")

    @staticmethod
    def abort_due_to_no_predictor_configuration(args):
        """
        Abort due to no predictor configuration for the specified predictor name.
        :param args: requests arguments.
        :type args: reqparse.Argument.
        :return: None.
        """
        abort(f"402", message=f"No predictor configuration found for {args['model']}")

    @staticmethod
    def abort_due_to_no_loadable_predictor(args):
        """
        Abort due to no predictor being loadable for the specified predictor name.
        :param args: requests arguments.
        :type args: reqparse.Argument.
        :return: None.
        """
        abort(f"403", message=f"No loadable predictor found for {args['model']}")

    @staticmethod
    def abort_due_to_unsupported_features_data_type(args):
        """
        Aborts due to unsupported features type.
        :param args: requests arguments.
        :type args: reqparse.Argument.
        :return: None.
        """
        abort(f"404", message=f"Features type unsupported (features: {args['features']})")

    @staticmethod
    def abort_due_to_no_features(args):
        """
        Aborts due to no features being present in the args.
        :param args: requests arguments.
        :type args: reqparse.Argument.
        :return: None.
        """
        abort(f"405", message=f"Features not present in {args['features']}")

    @staticmethod
    def abort_due_to_features_conversion_failed(args, e):
        """
        Aborts due to features conversion failed.
        :param args: requests arguments.
        :type args: reqparse.Argument.
        :param e: Exception alias.
        :type e: Exception.
        :return: None.
        """
        logger.exception(e)
        abort(f"406", message=f"Features conversion (args: {args}) failed")

    @staticmethod
    def abort_due_to_features_preprocessor_failed(args, e):
        """
        Aborts due to features preprocessor failed.
        :param args: requests arguments.
        :type args: reqparse.Argument.
        :param e: Exception alias.
        :type e: Exception.
        :return: None.
        """
        logger.exception(e)
        abort(f"407", message=f"Features preprocessor (args: {args}) failed")

    @staticmethod
    def abort_due_to_predictor_failed(args, e):
        """
        Aborts due to predictor failed.
        :param args: requests arguments.
        :type args: reqparse.Argument.
        :param e: Exception alias.
        :type e: Exception.
        :return: None.
        """
        logger.exception(e)
        abort(f"408", message=f"Predictor (args: {args}) failed")

    def prepare_predictor_configuration(self, args):
        """
        Prepares the predictor configuration given the input arguments.
        :param args: requests arguments.
        :type args: reqparse.Argument.
        :return: predictor configuration.
        """

        # Get the predictor model entity from the parsed model
        model_entity = PredictorModelEntity.from_dict(args)

        # Get the predictor model configuration from the database
        configuration = self.model_manager.get(model_name=model_entity["model"])

        # Handle no predictor configuration case
        if not configuration:
            self.abort_due_to_no_predictor_configuration(args)

        # Return the predictor configuration
        return configuration

    def prepare_predictor(self, predictor_configuration, args):
        """
        Prepares the predictor model given its configuration and the input arguments.
        :param predictor_configuration: predictor configuration.
        :type predictor_configuration: dict.
        :param args: requests arguments.
        :type args: reqparse.Argument.
        :return: predictor configuration.
        """
        try:
            return PredictorLoader().load(predictor_configuration)
        except NoLoadablePredictorException:
            self.abort_due_to_no_loadable_predictor(args)

    def prepare_features(self, args):
        """
        Prepares the features given the input arguments.
        :param args: requests arguments.
        :type args: reqparse.Argument.
        :return: loaded and pre-processed features.
        """
        try:
            return Features.from_request(args["features"]).as_dataframe
        except TypeError:
            self.abort_due_to_unsupported_features_data_type(args)
        except KeyError:
            self.abort_due_to_no_features(args)
        except Exception as e:
            self.abort_due_to_features_conversion_failed(args, e)

    def preprocess_features(self, features, predictor_configuration, args):
        """
        Pre-processes the features given the predictor configuration and the input arguments.
        :param features: features.
        :type features: pandas.DataFrame.
        :param predictor_configuration: predictor configuration.
        :type predictor_configuration: dict.
        :param args: requests arguments.
        :type args: reqparse.Argument.
        :return: loaded and pre-processed features.
        """
        try:
            return FeaturesPreprocessor(predictor_configuration).transform(features)
        except Exception as e:
            self.abort_due_to_features_preprocessor_failed(args, e)

    def post(self):
        """
        Handles the HTTP POST request of the predictor API. First, features are built from the request.
        Next the features are pre-processed via feature pre-processor, and finally, the prediction is
        performed using pre-trained predictor specified in the request model arg.
        :return: dict with the predicted value(s) and additional meta information.
        """

        # Parse the HTTP POST requests arguments (strict settings: all args must be specified)
        args = self.parser.parse_args(strict=True)

        # Validate the completeness of the input arguments
        if not all((args.get("features"), args.get("model"))):
            self.abort_due_to_incomplete_args(args)

        # Prepare the predictor configuration
        predictor_configuration = self.prepare_predictor_configuration(args)

        # Prepare the predictor model
        predictor = self.prepare_predictor(predictor_configuration, args)

        # Prepare the features
        #
        #  1. create the Features instance
        #  2. pre-process the feature values
        features = self.prepare_features(args)
        features = self.preprocess_features(features, predictor_configuration, args)

        # Predict the class
        try:
            predictions = predictor.predict(features)
        except Exception as e:
            self.abort_due_to_predictor_failed(args, e)
        else:

            # Responsify the predictions
            predictions = Predictions.from_predictions(predictions)
            predictions = predictions.as_response

            # Return the response
            return {
                "predictions": predictions,
                "features": args["features"],
                "model": args["model"]
            }
