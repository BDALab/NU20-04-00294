import os
import importlib
from api.common.logging import get_logger
from api.dsp.externals.exceptions import NoImportableFeaturesExtractorException


# Create the module-level importing logger
logger = get_logger("ImportFeaturesExtractionLibrary", propagate=True)


def import_features_extraction_library():
    """
    Imports the features extraction library specified in .env configuration file.
    :return: features extraction library.
    """

    # Extract the features extraction library specification from the environmental variables
    library_name = os.environ.get("FEATURES_EXTRACTION_LIBRARY")
    library_data = None

    # Check if the features extraction library is specified
    if not library_name:
        logger.error("Features extraction library not specified")
        return None

    # Try to load the library
    try:
        library_data = importlib.import_module(library_name)
    except ValueError:
        logger.error("Features extraction library not specified")
    except ModuleNotFoundError:
        logger.error("Features extraction library not installed")
    except Exception as e:
        logger.exception(f"Features extraction library cannot be loaded due to: {e}")
    finally:
        return library_data


def import_features_extractor(module):
    """
    Imports the features extractor from the features extraction library.
    :param module: module name.
    :type: str.
    :return: feature extractor if importable, exception otherwise.
    """
    try:
        return module.FeaturesExtractor
    except AttributeError:
        raise NoImportableFeaturesExtractorException
