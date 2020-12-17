import json


class PredictorModelEntity(object):
    """Class implementing the predictor model entity"""

    def __init__(self, data):
        """
        Initializes the PredictorModelEntity.
        :param data: data to be converted into the model entity data.
        :type data: dict.
        """
        self.data = data

    def __repr__(self):
        return self.data

    def __str__(self):
        return self.as_dict

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value

    def get(self, item):
        return self.as_dict.get(item)

    def set(self, key, value):
        self.data[key] = value

    @classmethod
    def from_dict(cls, data=None):
        """
        Initializes PredictorModelEntity from dict.
        :param data: data dict.
        :type data: dict.
        :return: class instance.
        """
        return cls(data) if data else None

    @classmethod
    def from_json(cls, data=None):
        """
        Initializes PredictorModelEntity from json.
        :param data: data json.
        :type data: json.
        :return: class instance.
        """
        return cls(json.loads(data)) if data else None

    @property
    def as_dict(self):
        """
        Returns the entity data as dict.
        :return: entity data as dict.
        """
        return dict(self.data) if not isinstance(self.data, dict) else self.data

    @property
    def as_json(self):
        """
        Returns the entity data as json.
        :return: entity data as json.
        """
        return json.dumps(self.as_dict)
