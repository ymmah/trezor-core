from trezor import res
from trezor import ui


class PinCancelled(Exception):
    pass


@ui.layout(delay=5000)
async def request_pin(code: int = None, device_label: str = '') -> str:
    from trezor.ui.confirm import ConfirmDialog, CONFIRMED
    from trezor.ui.pin import PinMatrix

    label = _get_label(code, device_label)

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
            raise PinCancelled()


def _get_label(code: int, device_label: str):
    from trezor.messages import PinMatrixRequestType
    if code is None:
        code = PinMatrixRequestType.Current
    if code == PinMatrixRequestType.NewFirst:
        label = 'Enter new PIN'
    elif code == PinMatrixRequestType.NewSecond:
        label = 'Enter PIN again'
    else:  # PinMatrixRequestType.Current
        if device_label:
            label = 'Unlock %s' % device_label
        else:
            label = 'Enter PIN'
    return label
