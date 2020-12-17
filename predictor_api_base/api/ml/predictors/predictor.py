import os
import glob
import ntpath
import pickle
from api.common.base import ObjectBase
from api.ml.predictors.exceptions import NoLoadablePredictorException


class PredictorLoader(ObjectBase):
    """Class implementing the predictor loader"""

    def __init__(self):
        """Initializes the PredictorLoader"""
        super().__init__()

    def load(self, configuration):
        """
        Loads the predictor.
        :param configuration: model configuration.
        :type configuration: dict.
        :return: loaded model.
        """

        # If the requested predictor model is not loadable raise an exception
        if configuration.get("name") not in self.models:
            raise NoLoadablePredictorException()

        # Return the initialized predictor
        return Predictor(configuration)

    @property
    def models(self):
        """
        Lists the models that are loadable.
        :return: list with the loadable model names (without extensions).
        """
        return [
            os.path.splitext(ntpath.basename(f))[0]
            for f in glob.glob(f"{self.models_path}**/*.{Predictor.extension}")
        ]


class Predictor(ObjectBase):
    """Class implementing the predictor"""

    # File-type extension used to serialize/deserialize the models
    extension = "pkl"

    def __init__(self, model_configuration):
        """
        Initializes the Predictor.
        :param model_configuration: configuration of the model to be loaded.
        :type model_configuration: dict.
        """
        super().__init__()

        # Initialize the model
        self._model_name = model_configuration.get("name")
        self._model_meta = model_configuration.get("meta")
        self._model_path = os.path.join(self.models_path, f"{self.model_name}")
        self._model_file = None

        # Load the model
        self.load()

    def __repr__(self):
        return self.model_name

    def __str__(self):
        return f"{self.model_path}.{self.extension}"

    def load(self):
        """
        Loads the predictor model.
        :return: None.
        """
        with open(self.__str__(), "rb") as file:
            self.model_file = pickle.load(file)

    def save(self):
        """
        Saves the predictor model.
        :return: None.
        """
        with open(self.__str__(), "wb") as f:
            pickle.dump(self.model_file, f)

    def predict(self, features):
        """
        Predicts the class(es).
        :param features: features.
        :type features: numpy.ndarray of pandas DataFrame.
        :return: predicted value(s).
        """
        return self.model_file.predict(features)

    def predict_proba(self, features):
        """
        Predicts the probability of the <features> belonging to the class(es).
        :param features: features.
        :type features: numpy.ndarray of pandas DataFrame.
        :return: predicted probability(ies).
        """
        return self.model_file.predict_proba(features)

    @property
    def model_name(self):
        """
        Returns the model name.
        :return: model name.
        """
        return self._model_name

    @property
    def model_meta(self):
        """
        Returns the model meta information.
        :return: model meta information.
        """
        return self._model_meta

    @property
    def model_path(self):
        """
        Returns the model path.
        :return: model path.
        """
        return self._model_path

    @model_path.setter
    def model_path(self, model_path):
        """
        Sets the model path.
        :param model_path:
        :return: None.
        """
        self._model_path = model_path

    @property
    def model_file(self):
        """
        Returns the model file.
        :return: model file.
        """
        return self._model_file

    @model_file.setter
    def model_file(self, model_file):
        """
        Sets the model file.
        :param model_file:
        :return: None.
        """
        self._model_file = model_file
