import os
import abc
from tinydb import TinyDB, Query
from api.common.base import ObjectBase
from api.database.entities import PredictorModelEntity


class ManagerBase(ObjectBase):
    """"Base class for database manager classes"""

    # Database-specific variables
    #
    #  1. database path
    #  2. database name (to be override by a sub-class)
    database_path = ObjectBase.database_path
    database_name = ""

    # Entity-specific variables
    supported_entity = None

    def __init__(self):
        """Initializes the ManagerBase"""
        super().__init__()

    def input(self, data):
        """
        Prepares input data to be stored via the manager.
        :param data: data to be prepared.
        :type data: dict-like object (must be supported, see: <self.validate_input>).
        :return: dict-like object.
        """
        return self.validate_input(data)

    def output(self, data):
        """
        Prepares output data to be returned via the manager.
        :param data: data to be prepared.
        :type data: dict-like object (must be supported, see: <self.validate_output>).
        :return: data dict.
        """
        return self.validate_output(data)

    def validate_input(self, data):
        """
        Validates the type of the data to be handled by the manager.
        :param data: object.
        :type data: <object>.
        :return: data.
        """
        if not isinstance(data, self.supported_entity):
            raise TypeError(f"Data must be of type '{self.supported_entity}' not '{type(data)}'")
        return data

    @staticmethod
    def validate_output(data):
        """
        Validates the type of the data to be returned by the manager.
        :param data: object.
        :type data: <object>.
        :return: data dict.
        """
        return (data if isinstance(data, dict) else dict(data)) if data else data

    @abc.abstractmethod
    def create(self, uid=None, data=None, **kwargs):
        """
        Creates a new record in the database (to be implemented by a sub-class).
        :param uid: unique identifier of a record.
        :type uid: str.
        :param data: data for a record.
        :type data: dict.
        :param kwargs: additional keyword arguments.
        :type kwargs: dict.
        :return: uid of the created record.
        """
        pass

    @abc.abstractmethod
    def read(self, uid=None, **kwargs):
        """
        Reads an existing record in the database (to be implemented by a sub-class).
        :param uid: unique identifier of a record.
        :type uid: str.
        :param kwargs: additional keyword arguments.
        :type kwargs: dict.
        :return: read record.
        """
        pass

    @abc.abstractmethod
    def update(self, uid=None, data=None, **kwargs):
        """
        Updates an existing record in the database (to be implemented by a sub-class).
        :param uid: unique identifier of a record.
        :type uid: str.
        :param data: data for a record.
        :type data: dict.
        :param kwargs: additional keyword arguments.
        :type kwargs: dict.
        :return: uid of the updated record.
        """
        pass

    @abc.abstractmethod
    def delete(self, uid=None, **kwargs):
        """
        Deletes an existing record in the database (to be implemented by a sub-class).
        :param uid: unique identifier of a record.
        :type uid: str.
        :param kwargs: additional keyword arguments.
        :type kwargs: dict.
        :return: uid of the deleted record.
        """
        pass

    @property
    def database(self):
        """
        Returns the database path.
        :return: database path.
        """
        return os.path.join(self.database_path, self.database_name)


class TinyDBManager(ManagerBase):
    """Class implementing the TinyDB manager"""

    # Database-specific variables
    database_name = "database.json"

    # Table-specific variables
    #
    #  1. table name
    #  2. cache size
    table_name = None
    cache_size = None

    def __init__(self):
        """Initializes the TinyDBManager"""
        super().__init__()

        # Initialize the database client
        self.client = TinyDB(self.database)

        # Initialize the table
        self.table = self.client.table(self.table_name, cache_size=self.cache_size)

        # Initialize the query object
        self.query = Query()

    @staticmethod
    def uid(uid):
        """
        Handles the uid with respect to its use in the queries.
        :param uid: uid.
        :type uid: Any(str, list, None).
        :return: list or None.
        """
        return ([uid] if not isinstance(uid, list) else uid) if uid else None

    def input(self, data):
        return super().input(data).as_dict

    def output(self, data):
        return super().output(data)

    def create(self, data=None, **kwargs):
        return self.table.insert(self.input(data))

    def read(self, uid=None, field_name="", field_value="", **kwargs):
        return self.output(self.table.get(self.query[field_name] == field_value, doc_id=uid))

    def update(self, uid=None, data=None, field_name="", field_value="", **kwargs):
        return self.table.update(self.input(data), self.query[field_name] == field_value, doc_ids=self.uid(uid))

    def delete(self, uid=None, field_name="", field_value="", **kwargs):
        return self.table.remove(self.query[field_name] == field_value, doc_ids=[uid])


class PredictorModelManager(TinyDBManager):
    """Class implementing the predictor model entity manager"""

    # Table-specific variables
    #
    #  1. table name
    #  2. cache size
    table_name = "predictor"
    cache_size = 100

    # Entity-specific variables
    supported_entity = PredictorModelEntity

    # Predictor-specific variables
    predictor_name = "name"

    def __init__(self):
        """Initializes the PredictorModelManager"""
        super().__init__()

        # Initialize the table
        self.table = self.client.table(self.table_name, cache_size=self.cache_size)

    def get(self, uid=None, model_name="", **kwargs):
        """
        Gets a model record.
        :param uid: unique identifier of a record.
        :type uid: str.
        :param model_name: name of the predictor model.
        :type model_name: str.
        :param kwargs: additional keyword arguments.
        :type kwargs: dict.
        :return: read model record.
        """
        return PredictorModelEntity.from_dict(self.read(uid, self.predictor_name, model_name, **kwargs))

    def set(self, uid=None, data=None, **kwargs):
        """
        Sets a model record (creates or updates a record depending on its existence).
        :param uid: unique identifier of a record.
        :type uid: str.
        :param data: data to be converted into a model record.
        :type data: ModelEntity.
        :param kwargs: additional keyword arguments.
        :type kwargs: dict.
        :return: uid of the created object.
        """
        if self.read(uid, self.predictor_name, data["name"], **kwargs):
            return self.update(uid, data, self.predictor_name, data["name"], **kwargs)
        else:
            return self.create(data)
