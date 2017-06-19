from typing import Callable, Coroutine, List, Optional
from trezor import log, loop, ui

_started = []  # type: List[Coroutine]
_default = None  # type: Optional[Coroutine]
_default_genfunc = None  # type: Optional[Callable[[], Coroutine]]


def start_default(genfunc: Callable[[], Coroutine]) -> None:
    global _default
    global _default_genfunc
    _default_genfunc = genfunc
    _default = _default_genfunc()
    log.info(__name__, 'start default %s', _default)
    loop.schedule_task(_default)
    ui.display.backlight(ui.BACKLIGHT_NORMAL)


def close_default() -> None:
    global _default
    if _default is not None:
        log.info(__name__, 'close default %s', _default)
        _default.close()
        _default = None


def start(workflow: Coroutine) -> None:
    close_default()
    _started.append(workflow)
    log.info(__name__, 'start %s', workflow)
    loop.schedule_task(_wrap(workflow))  # type: ignore # FIXME: https://github.com/python/typing/issues/441


async def _wrap(workflow: Coroutine):
    ui.display.backlight(ui.BACKLIGHT_NORMAL)
    try:
        return await workflow
    finally:
        _started.remove(workflow)
        if not _started and _default_genfunc is not None:
            start_default(_default_genfunc)
