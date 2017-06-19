from micropython import const
from typing import Any

import sys
import utime

NOTSET = const(0)  # type: int
DEBUG = const(10)  # type: int
INFO = const(20)  # type: int
WARNING = const(30)  # type: int
ERROR = const(40)  # type: int
CRITICAL = const(50)  # type: int

_leveldict = {
    DEBUG: ('DEBUG', '32'),
    INFO: ('INFO', '36'),
    WARNING: ('WARNING', '33'),
    ERROR: ('ERROR', '31'),
    CRITICAL: ('CRITICAL', '1;31'),
}

level = NOTSET  # type: int
color = True  # type: bool


def _log(name: str, mlevel: int, msg: str, *args: Any) -> None:
    if __debug__ and mlevel >= level:
        if color:
            fmt = '%d \x1b[35m%s\x1b[0m %s \x1b[' + \
                _leveldict[mlevel][1] + 'm' + msg + '\x1b[0m'
        else:
            fmt = '%d %s %s ' + msg
        print(fmt % ((utime.ticks_us(), name, _leveldict[mlevel][0]) + args))


def debug(name: str, msg: str, *args: Any) -> None:
    _log(name, DEBUG, msg, *args)


def info(name: str, msg: str, *args: Any) -> None:
    _log(name, INFO, msg, *args)


def warning(name: str, msg: str, *args: Any) -> None:
    _log(name, WARNING, msg, *args)


def error(name: str, msg: str, *args: Any) -> None:
    _log(name, ERROR, msg, *args)


def exception(name: str, exc: BaseException) -> None:
    _log(name, ERROR, 'exception:')
    sys.print_exception(exc)


def critical(name: str, msg: str, *args: Any) -> None:
    _log(name, CRITICAL, msg, *args)
