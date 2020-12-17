import numpy
import pandas
import json
import json_tricks


class Features(object):
    """Class implementing features (to built the request from the features)"""

    def __init__(self, features=None, rows=None, cols=None):
        """
        Initializes the Features.
        :param features: N-dimensional numpy array with the features.
        :type features: numpy ndarray.
        :param rows: row description (labels).
        :type rows: list.
        :param cols: column description (labels).
        :type cols: list.
        """

        # Handle the unsupported type exception
        if not isinstance(features, numpy.ndarray):
            raise TypeError(f"Features must be of type '{numpy.ndarray}' not '{type(features)}'")

        # Set the features and the descriptors (rows and columns labels)
        self.feat = features
        self.rows = rows if rows else list(range(self.feat.shape[0]))
        self.cols = cols if rows else list(range(self.feat.shape[1]))

    def __str__(self):
        return str(self.as_dict)

    @property
    def as_dict(self):
        """
        Returns features as dict.
        :return: dict with the features, and rows and columns labels.
        """
        return {"features": self.feat, "rows": self.rows, "cols": self.cols}

    @property
    def as_response(self):
        """
        Returns features as request JSON-serialized data.
        :return: JSON string with JSON-serialized features, and rows and columns labels.
        """
        feat = {"features": json_tricks.dumps(self.feat), "rows": self.rows, "cols": self.cols}
        feat = json.dumps(feat)
        return feat

    @classmethod
    def from_ndarray(cls, ndarray):
        """
        Creates Features instance from the numpy ndarray.
        :param ndarray: numpy ndarray with the features.
        :type ndarray: numpy.ndarray.
        :return: class instance.
        """

        # Handle the unsupported type exception
        if not isinstance(ndarray, numpy.ndarray):
            raise TypeError(f"Data must be of type '{numpy.ndarray}' not '{type(ndarray)}'")

        # Return the class instance
        return cls(ndarray, rows=None, cols=None)

    @classmethod
    def from_dataframe(cls, dataframe):
        """
        Creates Features instance from the pandas DataFrame.
        :param dataframe: pandas DataFrame with the features.
        :type dataframe: pandas.DataFrame.
        :return: class instance.
        """

        # Handle the unsupported type exception
        if not isinstance(dataframe, pandas.DataFrame):
            raise TypeError(f"Data must be of type '{pandas.DataFrame}' not '{type(dataframe)}'")

        # Return the class instance
        return cls(
            dataframe.values,
            rows=dataframe.index.to_list(),
            cols=dataframe.columns.to_list()
        )

    @classmethod
    def from_list(cls, array):
        """
        Creates Features instance from the list.
        :param array: list with the features.
        :type array: list.
        :return: class instance.
        """

        # Handle the unsupported type exception
        if not isinstance(array, list):
            raise TypeError(f"Data must be of type '{list}' not '{type(array)}'")

        # Return the class instance
        return cls(numpy.array(array), rows=None, cols=None)

    @classmethod
    def from_extracted_features(cls, features):
        """
        Creates Features instance from the extracted features (supported types).
        :param features: features.
        :type features: supported types (see <from_*) cls methods).
        :return: class instance.
        """

        # Return the class instance according to the type of the features
        if isinstance(features, numpy.ndarray):
            return Features.from_ndarray(features)
        if isinstance(features, pandas.DataFrame):
            return Features.from_dataframe(features)
        if isinstance(features, list):
            return Features.from_list(features)

        # Handle the unsupported type exception
        raise TypeError(f"Unsupported data type '{type(features)}'")
