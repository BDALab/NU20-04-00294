import numpy
import pandas
import json
import json_tricks


class Predictions(object):
    """Class implementing predictions (to built the request from the predictions)"""

    def __init__(self, predictions=None, rows=None, cols=None):
        """
        Initializes the Predictions.
        :param predictions: N-dimensional numpy array with the predictions.
        :type predictions: numpy ndarray.
        :param rows: row description (labels).
        :type rows: list.
        :param cols: column description (labels).
        :type cols: list.
        """

        # Handle the unsupported type exception
        if not isinstance(predictions, numpy.ndarray):
            raise TypeError(f"Predictions must be of type '{numpy.ndarray}' not '{type(Predictions)}'")

        # Set the predictions and the descriptors (rows and columns labels)
        self.pred = predictions
        self.rows = rows if rows else list(range(self.pred.shape[0]))
        self.cols = cols if rows else list(range(self.pred.shape[1]))

    def __str__(self):
        return str({"predictions": self.pred, "rows": self.rows, "cols": self.cols})

    @property
    def as_dict(self):
        """
        Returns predictions as dict.
        :return: dict with the predictions, and rows and columns labels.
        """
        return {"predictions": self.pred, "rows": self.rows, "cols": self.cols}

    def as_response(self):
        """
        Returns predictions as request JSON-serialized data.
        :return: JSON string with JSON-serialized predictions, and rows and columns labels.
        """
        pred = {"predictions": json_tricks.dumps(self.pred), "rows": self.rows, "cols": self.cols}
        pred = json.dumps(pred)
        return pred

    @classmethod
    def from_ndarray(cls, ndarray):
        """
        Creates Predictions instance from the numpy ndarray.
        :param ndarray: numpy ndarray with the predictions.
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
        Creates Predictions instance from the pandas DataFrame.
        :param dataframe: pandas DataFrame with the predictions.
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
        Creates Predictions instance from the list.
        :param array: list with the predictions.
        :type array: list.
        :return: class instance.
        """

        # Handle the unsupported type exception
        if not isinstance(array, list):
            raise TypeError(f"Data must be of type '{list}' not '{type(array)}'")

        # Return the class instance
        return cls(numpy.array(array), rows=None, cols=None)

    @classmethod
    def from_predictions(cls, predictions):
        """
        Creates Predictions instance from the predictions (supported types).
        :param predictions: predictions.
        :type predictions: supported types (see <from_*) cls methods).
        :return: class instance.
        """

        # Return the class instance according to the type of the predictions
        if isinstance(predictions, numpy.ndarray):
            return Predictions.from_ndarray(predictions)
        if isinstance(predictions, pandas.DataFrame):
            return Predictions.from_dataframe(predictions)
        if isinstance(predictions, list):
            return Predictions.from_list(predictions)

        # Handle the unsupported type exception
        raise TypeError(f"Unsupported data type '{type(predictions)}'")
