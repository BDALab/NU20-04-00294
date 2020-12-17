from flask_restful import Resource, reqparse, abort
from api.common.logging import get_logger
from api.dsp.externals.validations import import_features_extraction_library
from api.dsp.externals.validations import validate_features_extractor, import_features_extractor
from api.dsp.utilities.inputs import RawData, RawMeta
from api.dsp.utilities.outputs import Features


# Import the features extraction library
feature_extraction = import_features_extraction_library()

# Create the module-level featurizer resource logger
logger = get_logger("FeaturizerResource", propagate=True)


class FeaturizerResource(Resource):
    """Class implementing the featurizer API resource"""

    # Request arguments parser
    parser = reqparse.RequestParser()

    # Supported request arguments
    parser.add_argument("data", type=str, help="Dict with the raw data")
    parser.add_argument("meta", type=str, help="Dict with the raw data meta information")
    parser.add_argument("configuration", type=str, help="Dict with the features extraction configuration")

    @staticmethod
    def abort_due_to_incomplete_args(args):
        """
        Aborts due to incomplete requests arguments.
        :param args: requests arguments.
        :type args: reqparse.Argument.
        :return: None.
        """
        abort(f"401", message=f"Request args {args} (data and configuration must be provided)")

    @staticmethod
    def abort_due_to_not_importable_features_extractor(args):
        """
        Aborts due to not importable features extractor.
        :param args: requests arguments.
        :type args: reqparse.Argument.
        :return: None.
        """
        abort(f"402", message=f"Feature extractor is not importable (config: {args['configuration']})")

    @staticmethod
    def abort_due_to_unsupported_raw_data_type(args):
        """
        Aborts due to unsupported raw data type.
        :param args: requests arguments.
        :type args: reqparse.Argument.
        :return: None.
        """
        abort(f"403", message=f"Raw data type unsupported (data: {args['data']})")

    @staticmethod
    def abort_due_to_no_raw_data(args):
        """
        Aborts due to no raw data being present in the args.
        :param args: requests arguments.
        :type args: reqparse.Argument.
        :return: None.
        """
        abort(f"404", message=f"Raw data not present in {args['data']}")

    @staticmethod
    def abort_due_to_raw_data_conversion_failed(args, e):
        """
        Aborts due to raw data conversion failed.
        :param args: requests arguments.
        :type args: reqparse.Argument.
        :param e: Exception alias.
        :type e: Exception.
        :return: None.
        """
        logger.exception(e)
        abort(f"405", message=f"Raw data conversion (args: {args}) failed")

    @staticmethod
    def abort_due_to_unsupported_raw_meta_type(args):
        """
        Aborts due to unsupported raw data meta information type.
        :param args: requests arguments.
        :type args: reqparse.Argument.
        :return: None.
        """
        abort(f"406", message=f"Raw meta type unsupported (meta: {args['meta']})")

    @staticmethod
    def abort_due_to_raw_meta_conversion_failed(args, e):
        """
        Aborts due to raw data meta information failed.
        :param args: requests arguments.
        :type args: reqparse.Argument.
        :param e: Exception alias.
        :type e: Exception.
        :return: None.
        """
        logger.exception(e)
        abort(f"407", message=f"Raw meta conversion (args: {args}) failed")

    @staticmethod
    def abort_due_to_features_extractor_failed(args, e):
        """
        Aborts due to features extractor failed.
        :param args: requests arguments.
        :type args: reqparse.Argument.
        :param e: Exception alias.
        :type e: Exception.
        :return: None.
        """
        logger.exception(e)
        abort(f"408", message=f"Features extractor (args: {args}) failed")

    def prepare_raw_data(self, args):
        """
        Prepares the raw data for the features extraction.
        :param args: requests arguments.
        :type args: reqparse.Argument.
        :return: RawData instance.
        """
        try:
            return RawData.from_request(args["data"])
        except TypeError:
            self.abort_due_to_unsupported_raw_data_type(args)
        except KeyError:
            self.abort_due_to_no_raw_data(args)
        except Exception as e:
            self.abort_due_to_raw_data_conversion_failed(args, e)

    def prepare_raw_meta(self, args):
        """
        Prepares the raw data meta information for the features extraction.
        :param args: requests arguments.
        :type args: reqparse.Argument.
        :return: RawMeta instance.
        """
        try:
            return RawMeta.from_request(args.get("meta"))
        except TypeError:
            self.abort_due_to_unsupported_raw_meta_type(args)
        except Exception as e:
            self.abort_due_to_raw_meta_conversion_failed(args, e)

    def prepare_features_extractor(self, args):
        """
        Prepares the features extractor for the features extraction.
        :param args: requests arguments.
        :type args: reqparse.Argument.
        :return: FeaturesExtractor instance.
        """

        # Validate the features extractor
        if not validate_features_extractor(feature_extraction):
            self.abort_due_to_not_importable_features_extractor(args)

        # Import the features extractor
        features_extractor = import_features_extractor(feature_extraction)

        # Return the features extractor
        return features_extractor(args["configuration"])

    def post(self):
        """
        Handles the HTTP POST request of the featurizer API. Raw data are processed and featurized
        by the features extraction library specified in the <.env> file. Every features-extraction
        specific nuance should be handled by the specific features extraction library. The API
        expects the features extraction library to provide a class <FeaturesExtractor> with
        the <compute> method. For more information, about the features extraction interface
        see the interface: <../dsp/interfaces/features_extraction>.
        :return: dict with the extracted feature(s) and additional meta information.
        """

        # Parse the HTTP POST requests arguments (loose settings: all args must not be specified)
        args = self.parser.parse_args(strict=False)

        # Validate the completeness of the input arguments
        if not all((args.get("data"), args.get("configuration"))):
            self.abort_due_to_incomplete_args(args)

        # Prepare the features extraction components
        #
        #  1. raw data
        #  2. raw data meta information
        raw_data = self.prepare_raw_data(args)
        raw_meta = self.prepare_raw_meta(args)

        # Prepare the features extractor
        features_extractor = self.prepare_features_extractor(args)

        # Extract the features
        try:
            features = features_extractor.compute(raw_data.as_dataframe, **raw_meta.as_dict)
        except Exception as e:
            self.abort_due_to_features_extractor_failed(args, e)
        else:

            # Responsify the features
            features = Features.from_extracted_features(features)
            features = features.as_response

            # Return the response
            return {
                "configuration": args["configuration"],
                "data": args["data"],
                "features": features,
            }
