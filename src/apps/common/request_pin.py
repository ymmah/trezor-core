from trezor import res
from trezor import ui
from trezor import TrezorException

@ui.layout(delay=5000)
async def request_pin(label: str = None) -> str:
    from trezor.messages.FailureType import PinCancelled
    from trezor.ui.confirm import ConfirmDialog, CONFIRMED
    from trezor.ui.pin import PinMatrix

    if label is None:
        label = 'Enter PIN'

    def onchange():
        c = dialog.cancel
        if matrix.pin:
            c.content = res.load(ui.ICON_CLEAR)
        else:
            c.content = res.load(ui.ICON_LOCK)
        c.taint()
        c.render()

    ui.display.clear()
    matrix = PinMatrix(label, with_zero=True)
    matrix.onchange = onchange
    dialog = ConfirmDialog(matrix)
    dialog.cancel.area = ui.grid(12)
    dialog.confirm.area = ui.grid(14)
    matrix.onchange()

    while True:
        result = await dialog
        if result == CONFIRMED:
            return matrix.pin
        elif result != CONFIRMED and matrix.pin:
            matrix.change('')
            continue
        else:
            raise TrezorException(PinCancelled, 'PIN entry cancelled')
