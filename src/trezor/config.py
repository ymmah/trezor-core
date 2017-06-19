from trezorconfig import Config

_config = Config()


def get(app: int, key: int) -> bytes:
    return _config.get(app, key)


def set(app: int, key: int, value: bytes) -> None:
    return _config.set(app, key, value)


def wipe() -> None:
    return _config.wipe()
