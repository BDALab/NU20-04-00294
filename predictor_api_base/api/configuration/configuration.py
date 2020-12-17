import os
import json


class ConfigurationBase(object):
    """Base class for configuration classes"""

    def __init__(self, configuration_path):
        """
        Initializes the ConfigurationBase.
        :param configuration_path: configuration dir path.
        :type configuration_path: str.
        """
        self.configuration_path = configuration_path

    @staticmethod
    def read(path):
        """
        Reads the configuration defined by the full-path (if it's existing and accessible).
        :param path: configuration file path.
        :type path: str.
        :return: read configuration.
        """
        if os.path.isfile(path) and os.access(path, os.R_OK):
            with open(path, "r") as f:
                return json.load(f)

    def load(self):
        """
        Loads the configuration.
        :return: loaded configuration dict.
        """
        return self.read(self.configuration_file)

    @property
    def configuration_file(self):
        """
        Returns the configuration file path.
        :return: configuration file path.
        """
        return None


class APIConfiguration(ConfigurationBase):
    """Class implementing API configuration"""

    def __init__(self, configuration_path):
        """
        Initializes the APIConfiguration.
        :param configuration_path: configuration file(s) path.
        :type configuration_path: str.
        """
        super().__init__(configuration_path)

    @property
    def configuration_file(self):
        return os.path.join(self.configuration_path, "api.json")


class MLConfiguration(ConfigurationBase):
    """Class implementing ML configuration"""

    def __init__(self, configuration_path):
        """
        Initializes the MLConfiguration.
        :param configuration_path: configuration file(s) path.
        :type configuration_path: str.
        """
        super().__init__(configuration_path)

    @property
    def configuration_file(self):
        return os.path.join(self.configuration_path, "ml.json")


class LoggingConfiguration(ConfigurationBase):
    """Class implementing logging configuration"""

    def __init__(self, configuration_path):
        """
        Initializes the LoggingConfiguration.
        :param configuration_path: configuration file(s) path.
        :type configuration_path: str.
        """
        super().__init__(configuration_path)

    @property
    def configuration_file(self):
        return os.path.join(self.configuration_path, "logging.json")
