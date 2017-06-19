from typing import Any, Optional


class Hmac:

    def __init__(self, key: bytes, msg: Optional[bytes], digestmod: Any) -> None:
        self._digestmod = digestmod
        self._inner = digestmod()
        self.digest_size = self._inner.digest_size
        self.block_size = self._inner.block_size
        if len(key) > self.block_size:
            self._key = digestmod(key).digest()
        else:
            self._key = key + bytes(self.block_size - len(key))
        self._inner.update(bytes((x ^ 0x36) for x in self._key))
        if msg is not None:
            self.update(msg)

    def update(self, msg: bytes) -> None:
        '''
        Update the context with data.
        '''
        self._inner.update(msg)

    def digest(self) -> bytes:
        '''
        Returns the digest of processed data.
        '''
        outer = self._digestmod()
        outer.update(bytes((x ^ 0x5C) for x in self._key))
        outer.update(self._inner.digest())
        return outer.digest()  # type: ignore # FIXME: digestmod type
