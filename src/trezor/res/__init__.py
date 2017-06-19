from typing import *

try:
    from .resources import resdata
except ImportError:
    resdata = {}


def load(name: str) -> bytes:
    '''
    Loads resource of a given name as bytes.
    '''
    if name in resdata:
        return resdata[name]
    with open(name, 'rb') as f:  # type: IO[bytes]
        return f.read()


def gettext(message: str) -> str:
    '''
    Returns localized string. This function is aliased to _.
    '''
    return message


_ = gettext
