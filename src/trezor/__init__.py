import trezorconfig as config
import trezorio as io
from trezor.wire import FailureError

class TrezorException(FailureError): pass
