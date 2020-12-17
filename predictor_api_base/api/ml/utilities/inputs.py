import numpy
import pandas
import json
import json_tricks


class Features(object):
    """Class implementing features (to built the features from the request)"""

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
        return str({"features": self.as_ndarray, "rows": self.rows, "cols": self.cols})

    @property
    def as_ndarray(self):
        """
        Returns features as numpy ndarray.
        :return: numpy ndarray with the features.
        """
        return self.feat

    @property
    def as_dataframe(self):
        """
        Returns features as pandas DataFrame.
        :return: pandas DataFrame with the features.
        """
        return pandas.DataFrame(self.as_ndarray, index=self.rows, columns=self.cols)

    @property
    def as_list(self):
        """
        Returns features as list.
        :return: list with the features.
        """
        return self.as_ndarray.tolist()

    @classmethod
    def from_request(cls, req):
        """
        Creates Features instance from the JSON-serialized data and additional information.
        :param req: dict with the JSON-serialized features and additional information.
        :type req: str.
        :return: class instance.
        """

        # Handle the unsupported type exception
        if not isinstance(req, str):
            raise TypeError(f"Features must be of type '{str}' not '{type(req)}'")

        # Convert the JSON-serialized request string into dict
        req = json.loads(req)

        # Return the class instance
        return cls(
            json_tricks.loads(req["features"]),
            rows=req.get("rows"),
            cols=req.get("cols")
        )
