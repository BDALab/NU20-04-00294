from pathlib import Path
from functools import wraps
from datetime import datetime
from api.common.structure import *


def ensure_database_dir():
    """Ensures that the full-path to database directory is created"""
    Path(database_path).mkdir(parents=True, exist_ok=True)


def ensure_models_dir():
    """Ensures that the full-path to ml models directory is created"""
    Path(models_path).mkdir(parents=True, exist_ok=True)


def ensure_logs_dir():
    """Ensures that the full-path to logging files directory is created"""
    Path(logging_path).mkdir(parents=True, exist_ok=True)


def ensure_structure(database_dir=True, models_dir=True, logs_dir=True):
    """
    Ensures the structure of the directories excluded from the version control.
    :param database_dir: database directory.
    :type database_dir: bool.
    :param models_dir: ml models directory.
    :type models_dir: bool.
    :param logs_dir: logs directory.
    :type logs_dir: bool.
    :return: None.
    """
    if database_dir:
        ensure_database_dir()
    if models_dir:
        ensure_models_dir()
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
