from logging import INFO
from vulcan.core.config import config

TRACE_VALUE = "TRACE"
DEBUG_VALUE = "DEBUG"
INFO_VALUE = "INFO"
WARN_VALUE = "WARN"
ERROR_VALUE = "ERROR"

LOG_LEVEL = str(config.LOG_LEVEL).upper()
# LOG_LEVEL = INFO_VALUE


def trace(*message):
    if trace_enabled():
        print(*message)


def debug(*message):
    if debug_enabled():
        print(*message)


def info(*message):
    if info_enabled():
        print(*message)


def warn(*message):
    if warn_enabled():
        print(*message)


def error(*message):
    if error_enabled():
        print(*message)


def trace_enabled():
    if LOG_LEVEL == TRACE_VALUE:
        return True
    return False


def debug_enabled():
    if LOG_LEVEL == DEBUG_VALUE or trace_enabled():
        return True
    return False


def info_enabled():
    if LOG_LEVEL == INFO_VALUE or debug_enabled():
        return True
    return False


def warn_enabled():
    if LOG_LEVEL == WARN_VALUE or info_enabled():
        return True
    return False


def error_enabled():
    if LOG_LEVEL == ERROR_VALUE or warn_enabled():
        return True
    return False
