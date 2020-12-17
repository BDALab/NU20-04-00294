import time
from datetime import datetime
from api.common.structure import *


class EventBase(object):
    """Class implementing event base"""

    def log(self, text):
        """
        Logs an event with input text and additional info: time, PID, and class name.
        :param text: input text to be logged.
        :type text: str.
        :return: None.
        """
        print(f"Event: {datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')}"
              f" - {os.getppid()}"
              f" - {self.__class__.__name__}"
              f" - {text}")


class ObjectBase(object):
    """class implementing object base"""

    # Project structure paths
    #
    #  1. configuration
    #  2. dsp
    #  3. resources

    # 1. configuration path
    configuration_path = configuration_path

    # 2. dsp path
    dsp_path = dsp_path

    # 3. resources path
    resources_path = resources_path
