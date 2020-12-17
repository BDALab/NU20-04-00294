import pandas
from sklearn.base import BaseEstimator


class FeaturesRenamer(BaseEstimator):
    """Class implementing features renamer"""

    # Label to be used to name the feature pre-processing step
    label = "feature_mask"

    def __init__(self, replacement):
        """
        Initializes the FeaturesRenamer.
        :param replacement: feature names to be used to rename the features.
        :type replacement: dict.
        """
        self.replacement = replacement

    def transform(self, X):
        """
        Transforms the features (feature names are renamed with the replacement).
        :param X: features.
        :type X: pandas.DataFrame.
        :return: transformed features.
        """
        return X.rename(columns=self.replacement)


class MissingFeaturesAdder(BaseEstimator):
    """Class implementing missing features adder"""

    # Label to be used to name the feature pre-processing step
    label = "feature_names"

    def __init__(self, features):
        """
        Initializes the MissingFeaturesAdder.
        :param features: features to be used in the updated data.
        :type features: list.
        """
        self.features = features

    def transform(self, X):
        """
        Transforms the features (missing features are added as NaNs).
        :param X: features.
        :type X: pandas.DataFrame.
        :return: transformed features.
        """
        return pandas.DataFrame(X, columns=self.features)


class MissingFeaturesImputer(BaseEstimator):
    """Class implementing missing features imputer"""

    # Label to be used to name the feature pre-processing step
    label = "feature_defaults"

    def __init__(self, replacement):
        """
        Initializes the MissingFeaturesImputer.
        :param replacement: features: values to be used when a missing values are found.
        :type replacement: dict.
        """
        self.replacement = replacement

    def transform(self, X):
        """
        Transforms the features (missing features are imputed with the replacement).
        :param X: features.
        :type X: pandas.DataFrame.
        :return: transformed features.
        """
        return X.fillna(value=self.replacement)


class FeaturesPreprocessorStep(dict):
    """Class implementing features preprocessor step (for convenience)"""

    def __init__(self, info):
        """
        Initializes the FeaturesPreprocessorStep.
        :param info: information to be used.
        :type info: dict.
        """
        super().__init__(info)

        # Update the namespace by the information dict
        self.__dict__ = self

    @property
    def meta(self):
        """
        Returns the pre-processing step meta information.
        :return: pre-processing step meta information.
        """
        try:
            return self["meta"]
        except KeyError:
            return None

    @property
    def worker(self):
        """
        Returns the pre-processing step worker (class)
        :return: pre-processing step worker.
        """
        try:
            return self["worker"]
        except KeyError:
            return None


class FeaturesPreprocessor(BaseEstimator):
    """Class implementing features preprocessor (implemented as sklearn's estimator)"""

    # Pre-processing mapping
    processing_map = {

        # Renaming the feature names (columns) according to the mapping
        "rename_features": {
            "meta": FeaturesRenamer.label,
            "worker": FeaturesRenamer
        },

        # Adding the missing feature columns (NaNs)
        "add_missing_features": {
            "meta": MissingFeaturesAdder.label,
            "worker": MissingFeaturesAdder
        },

        # Filling the missing features (NaNs) with default values
        "input_missing_values": {
            "meta": MissingFeaturesImputer.label,
            "worker": MissingFeaturesImputer
        }
    }

    # Pre-processing config field
    processing_field = "preprocessing"

    def __init__(self, predictor_configuration, inline_update=False):
        """
        Initializes the FeaturesPreprocessor.
        :param predictor_configuration: predictor configuration to be used to pre-process the data.
        :type predictor_configuration: dict.
        :param inline_update: inline (inplace) data update.
        :type inline_update: bool.
        """
        self.configuration = predictor_configuration
        self.inline_update = inline_update

    def transform(self, X):
        """
        Transforms the features.
        :param X: features.
        :type X: pandas.DataFrame.
        :return: transformed features.
        """

        # If no pre-processing is to be applied, return the original data
        if not self.configuration.get(self.processing_field):
            return X

        # Handle inline (inplace) data updating
        data = X.copy() if not self.inline_update else X

        # Pre-process the data according to the configuration
        for step in self.configuration.get(self.processing_field):
            if step in self.processing_map:

                # Get the pre-processing information
                processing = self.processing_map[step]
                processing = FeaturesPreprocessorStep(processing)

                # Use the pre-processing step
                if processing.meta in self.configuration:
                    data = processing.worker(self.configuration[processing.meta]).transform(data)

        # Return the pre-processed data
        return data
