from typing import Dict, Optional
import utime
from micropython import const
from trezor import ui


DEFAULT_LOADER = {
    'bg-color': ui.BLACK,
    'fg-color': ui.WHITE,
    'icon': None,
    'icon-fg-color': None,
}
DEFAULT_LOADER_ACTIVE = {
    'bg-color': ui.BLACK,
    'fg-color': ui.ACTIVE_GREEN,
    'icon': None,
    'icon-fg-color': None,
}

_LOADER_MSEC = const(1000)


class Loader(ui.Widget):

    def __init__(self,
                 normal_style: Dict = None,
                 active_style: Dict = None) -> None:
        self.start_ticks_ms = 0
        self.normal_style = normal_style or DEFAULT_LOADER
        self.active_style = active_style or DEFAULT_LOADER_ACTIVE

    def start(self) -> None:
        self.start_ticks_ms = utime.ticks_ms()
        ui.display.bar(0, 32, 240, 240 - 80, ui.BLACK)

    def stop(self) -> bool:
        ui.display.bar(0, 32, 240, 240 - 80, ui.BLACK)
        ticks_diff = utime.ticks_ms() - self.start_ticks_ms
        self.start_ticks_ms = 0
        return ticks_diff >= _LOADER_MSEC

    def is_active(self) -> bool:
        return self.start_ticks_ms == 0

    def render(self) -> None:
        progress = min(utime.ticks_ms() - self.start_ticks_ms, _LOADER_MSEC)
        if progress == _LOADER_MSEC:
            style = self.active_style
        else:
            style = self.normal_style
        if style['icon'] is None:
            ui.display.loader(  # type: ignore # suppress the dict lookup failure
                progress, -8, style['fg-color'], style['bg-color'])
        elif style['icon-fg-color'] is None:
            ui.display.loader(  # type: ignore # suppress the dict lookup failure
                progress, -8, style['fg-color'], style['bg-color'], style['icon'])
        else:
            ui.display.loader(  # type: ignore # suppress the dict lookup failure
                progress, -8, style['fg-color'], style['bg-color'], style['icon'], style['icon-fg-color'])
