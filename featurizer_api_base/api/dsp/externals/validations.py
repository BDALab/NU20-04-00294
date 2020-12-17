from api.dsp.externals.exceptions import NoImportableFeaturesExtractorException
from api.dsp.externals.imports import import_features_extraction_library, import_features_extractor


def validate_features_availability():
    """
    Validates the availability of the features extraction library.
    :return: True if available, False instead.
    """
    return True if import_features_extraction_library() else False


def validate_features_extractor(module):
    """
    Validates that the features extractor is loadable from the features extraction library.
    :param module: module name.
    :type: str.
    :return: True if importable, False instead.
    """
    try:
        import_features_extractor(module)
    except NoImportableFeaturesExtractorException:
        return False
    else:
        return True
