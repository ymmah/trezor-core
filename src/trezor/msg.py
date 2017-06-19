from typing import List, Union
from trezormsg import Msg, USB, HID, VCP

_msg = Msg()


def init_usb(usb: USB, ifaces: List[Union[HID, VCP]]) -> None:
    return _msg.init_usb(usb, ifaces)


def select(timeout_us: int) -> tuple:
    return _msg.select(timeout_us)


def send(iface: int, message: bytes) -> int:
    return _msg.send(iface, message)
