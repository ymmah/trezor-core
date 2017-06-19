from typing import *
from micropython import const
from trezor import loop
from trezor.ui import Widget
from .button import Button, BTN_CLICKED, BTN_STARTED
from .button import CONFIRM_BUTTON, CONFIRM_BUTTON_ACTIVE
from .button import CANCEL_BUTTON, CANCEL_BUTTON_ACTIVE
from .loader import Loader

CONFIRMED = const(1)
CANCELLED = const(2)


class ConfirmDialog(Widget):

    def __init__(self,
                 content: Widget = None,
                 confirm: str = 'Confirm',
                 cancel: str = 'Cancel') -> None:
        self.content = content
        if cancel is not None:
            self.confirm = Button((121, 240 - 48, 119, 48), confirm,
                                  normal_style=CONFIRM_BUTTON,
                                  active_style=CONFIRM_BUTTON_ACTIVE)
            self.cancel = Button((0, 240 - 48, 119, 48), cancel,
                                 normal_style=CANCEL_BUTTON,
                                 active_style=CANCEL_BUTTON_ACTIVE)
        else:
            self.cancel = None
            self.confirm = Button((0, 240 - 48, 240, 48), confirm,
                                  normal_style=CONFIRM_BUTTON,
                                  active_style=CONFIRM_BUTTON_ACTIVE)

    def render(self) -> None:
        self.confirm.render()
        if self.cancel is not None:
            self.cancel.render()

    def touch(self, event: int, pos: Tuple[int, int]) -> Optional[int]:
        if self.confirm.touch(event, pos) == BTN_CLICKED:
            return CONFIRMED

        if self.cancel is not None:
            if self.cancel.touch(event, pos) == BTN_CLICKED:
                return CANCELLED

    async def __iter__(self):  # type: ignore
        return await loop.Wait((super().__iter__(), self.content))


class HoldToConfirmDialog(Widget):

    def __init__(self,
                 content: Widget = None,
                 hold: str = 'Hold to confirm',
                 *args: Any,
                 **kwargs: Any) -> None:
        self.button = Button((0, 240 - 48, 240, 48), hold,
                             normal_style=CONFIRM_BUTTON,
                             active_style=CONFIRM_BUTTON_ACTIVE)
        self.content = content
        self.loader = Loader(*args, **kwargs)

    def render(self) -> None:
        if self.loader.is_active():
            self.loader.render()
        elif self.content is not None:
            self.content.render()
        self.button.render()

    def touch(self, event: int, pos: Tuple[int, int]) -> Optional[int]:
        button = self.button
        was_started = button.state & BTN_STARTED
        button.touch(event, pos)
        is_started = button.state & BTN_STARTED
        if is_started:
            if not was_started:
                self.loader.start()
        else:
            if was_started:
                if self.loader.stop():
                    return CONFIRMED
        if self.content is not None:
            return self.content.touch(event, pos)

    async def __iter__(self):  # type: ignore
        return await loop.wait((self._render_loop(), self._event_loop()))

    def _render_loop(self) -> Generator:
        sleep = loop.sleep(1000000 // 60)
        while True:
            self.render()
            yield sleep

    def _event_loop(self) -> Generator:
        touch = loop.select(loop.TOUCH)
        while True:
            event, *pos = yield touch
            result = self.touch(event, pos)
            if result is not None:
                return result
