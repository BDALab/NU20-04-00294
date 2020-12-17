import abc


class FeaturesExtractorInterface(object):
    """Class implementing features extractor interface (to compute the features from raw data)"""

    def __init__(self, settings=None):
        """
        Initializes the FeaturesExtractorInterface.
        :param settings: settings for the feature extraction.
        :type settings: dict.
        """
        super().__init__()

        # Set the feature extraction settings
        self.settings = settings

    def __str__(self):
        return str(self.settings)

    def __call__(self, raw_data, **kwargs):
        return self.extract(raw_data, **kwargs)

    @abc.abstractmethod
    def extract(self, df, **kwargs):
        """
        Extracts the features from the input raw data. The method is to be implemented inside
        the feature extractor class. The output features should be computed according to the
        settings provided during the initialization.

        Input(s)/output(s):
        The input formatting must be compatible with <../utilities/inputs.RawData>.
        The output formatting must be compatible with <../utilities/outputs.Features>.

        :param df: raw data.
        :type df: pandas.DataFrame.
        :param kwargs: additional keyword arguments.
        :type kwargs: dict.
        :return: pandas.DataFrame.
        """
        pass
