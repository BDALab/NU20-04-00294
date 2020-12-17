from pathlib import Path
from functools import wraps
from datetime import datetime
from api.common.structure import *


def ensure_logs_dir():
    """Ensures that the full-path to logging files directory is created"""
    Path(logging_path).mkdir(parents=True, exist_ok=True)


def ensure_structure(logs_dir=True):
    """
    Ensures the structure of the directories excluded from the version control.
    :param logs_dir: logs directory.
    :type logs_dir: bool.
    :return: None.
    """
    if logs_dir:
        ensure_logs_dir()


def measure_runtime(method):
    """
    Decorator that measures the runtime of the <method>.
    :param method: function to decorate.
    :type method: callable.
    :return: decorated function.
    """

    @wraps(method)
    def measure(*args, **kwargs):
        s = datetime.now()
        r = method(*args, **kwargs)
        f = datetime.now()
        d = (f - s)
        if d.microseconds > 0.0000:
            print(f"Execution of <{method.__name__}> finished (runtime): {d}")
        return r
    return measure
