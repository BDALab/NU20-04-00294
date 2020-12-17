import numpy
import pandas
import json
import json_tricks


class RawData(object):
    """Class implementing raw data (to built the raw data from the request)"""

    def __init__(self, data, rows=None, cols=None):
        """
        Initializes the RawData.
        :param data: N-dimensional numpy array with the raw data.
        :type data: numpy ndarray.
        :param rows: row description (labels).
        :type rows: list.
        :param cols: column description (labels).
        :type cols: list.
        """

        # Handle the unsupported type exception
        if not isinstance(data, numpy.ndarray):
            raise TypeError(f"Data must be of type '{numpy.ndarray}' not '{type(data)}'")

        # Set the raw data and the descriptors (rows and columns labels)
        self.data = data
        self.rows = rows if rows else list(range(self.data.shape[0]))
        self.cols = cols if rows else list(range(self.data.shape[1]))

    def __str__(self):
        return str({"data": self.as_ndarray, "rows": self.rows, "cols": self.cols})

    @property
    def as_ndarray(self):
        """
        Returns raw data as numpy ndarray.
        :return: numpy ndarray with the raw data.
        """
        return self.data

    @property
    def as_dataframe(self):
        """
        Returns raw data as pandas DataFrame.
        :return: pandas DataFrame with the raw data.
        """
        return pandas.DataFrame(self.as_ndarray, index=self.rows, columns=self.cols)

    @property
    def as_list(self):
        """
        Returns raw data as list.
        :return: list with the raw data.
        """
        return self.as_ndarray.tolist()

    @classmethod
    def from_request(cls, req):
        """
        Creates RawData instance from the JSON-serialized data and additional information.
        :param req: dict with the JSON-serialized data and additional information.
        :type req: str.
        :return: class instance.
        """

        # Handle the unsupported type exception
        if not isinstance(req, str):
            raise TypeError(f"Data must be of type '{str}' not '{type(req)}'")

        # Convert the JSON-serialized request string into dict
        req = json.loads(req)

        # Return the class instance
        return cls(
            json_tricks.loads(req["data"]),
            rows=req.get("rows"),
            cols=req.get("cols")
        )


class RawMeta(object):
    """Class implementing raw data meta information (to built the raw data from the request)"""

    def __init__(self, meta):
        """
        Initializes the RawMeta.
        :param meta: dict with the raw data meta information.
        :type meta: dict.
        """

        # Handle the unsupported type exception
        if not isinstance(meta, dict):
            raise TypeError(f"Meta must be of type '{dict}' not '{type(meta)}'")

        # Set the raw data meta information
        self.meta = meta

    def __str__(self):
        return str({"meta": self.as_dict})

    @property
    def as_dict(self):
        """
        Returns raw data meta information as dict.
        :return: dict with the raw data meta information.
        """
        return self.meta

    @property
    def as_json(self):
        """
        Returns raw data meta information as JSON-serialized data.
        :return: JSON string with the raw data meta information.
        """
        return json.dumps(self.as_dict)

    @classmethod
    def from_request(cls, req=None):
        """
        Creates RawMeta instance from the JSON-serialized data meta information.
        :param req: dict with the JSON-serialized data meta information.
        :type req: str.
        :return: class instance.
        """

        # Handle no meta information case
        if req is None:
            return cls({})

        # Handle the unsupported type exception
        if not isinstance(req, str):
            raise TypeError(f"Meta must be of type '{str}' not '{type(req)}'")

        # Convert the JSON-serialized request string into dict
        req = json.loads(req)

        # Return the class instance
        return cls(req)
