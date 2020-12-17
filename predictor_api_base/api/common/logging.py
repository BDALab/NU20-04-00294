import os
import sys
import logging
from datetime import datetime
from api.common.structure import configuration_path, logging_path
from api.configuration.configuration import LoggingConfiguration


def get_logger(name, propagate=False):
    """
    Gets the basic logger with the specified name and the propagation rule.
    :param name: name of the logger.
    :type name: str.
    :param propagate: logger propagation.
    :type propagate: bool.
    :return: Logger instance.
    """

    # Get the logger
    logger = logging.getLogger(name)

    # Set the propagation rule
    logger.propagate = propagate

    # Return the logger
    return logger


def configure_logging():
    """Configures basic logging"""

    # Load the logging configuration
    logging_config = LoggingConfiguration(configuration_path).load()

    # Configure the basic logging
    logging.basicConfig(
        filename=os.path.join(logging_path, f"{datetime.utcnow().strftime(logging_config['filename'])}.log"),
        filemode=logging_config["filemode"],
        format=logging_config["format"],
        datefmt=logging_config["datefmt"],
        level=logging.INFO)


class LoggerBase(object):
    """Class implementing base logging"""

    def __init__(self, logger_name=None):
        """
        Initializes the LoggerBase.
        :param logger_name: name of the logger to be used in the logs.
        :type logger_name: str.
        """

        # Create a custom logger
        self.logger = logging.getLogger(logger_name if logger_name else self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def exception(self, msg, *args, exc_info=True, **kwargs):
        self.logger.exception(msg, *args, exc_info=exc_info, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)


class ConsoleLogger(LoggerBase):
    """Class implementing console logging"""

    def __init__(self, logger_name=None):
        """
        Initializes the ConsoleLogger.
        :param logger_name: name of the logger to be used in the logs.
        :type logger_name: str.
        """
        super().__init__(logger_name)

        # Prepare the handler
        self.c_handler_attr = sys.stdout

        # Create handler
        self.c_handler = logging.StreamHandler(self.c_handler_attr)

        # Create formatter
        self.c_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        # Add the formatter to handler
        self.c_handler.setFormatter(self.c_format)

        # Add the handler to the logger
        self.logger.addHandler(self.c_handler)


class FileLogger(LoggerBase):
    """Class implementing file logging"""

    def __init__(self, logger_name=None, log_dir=logging_path):
        """
        Initializes the FileLogger.
        :param logger_name: name of the logger to be used in the logs.
        :type logger_name: str.
        :param log_dir: file-path to the logging file.
        :type log_dir: str.
        """
        super().__init__(logger_name)

        # Prepare the handler
        self.f_handler_attr = os.path.join(log_dir, f"{datetime.utcnow().strftime('%B-%d-%Y_%H-%M-%S')}.log")

        # Create handler
        self.f_handler = logging.FileHandler(self.f_handler_attr)

        # Create formatter
        self.f_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        # Add the formatter to handler
        self.f_handler.setFormatter(self.f_format)

        # Add the handler to the logger
        self.logger.addHandler(self.f_handler)
