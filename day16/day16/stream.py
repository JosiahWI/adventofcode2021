from typing import Optional, Union

class Stream:

    def __init__(self, raw_hex: str) -> None:
        self._data = bin(int(raw_hex, 16))[2:].zfill(len(raw_hex) * 4)
        self._end = len(self._data) - 1
        self._read_ptr = 0

    def tell(self) -> Optional[int]:
        if self._read_ptr >= self._end:
            return None
        return self._read_ptr

    def read(self, bits: Optional[int] = None,
             zfill_align: Optional[int] = None,
             raw: bool = False) -> Optional[int]:
        if self._read_ptr >= self._end:
            return None

        if bits is not None:
            res = self._data[self._read_ptr:self._read_ptr + bits]
            self._read_ptr += bits
        else:
            res = self._data[self._read_ptr:]
            self._read_ptr = self._end

        if zfill_align is not None:
            pad = len(res) % zfill_align
            res = res.zfill(len(res) + pad)

        return int(res, 2)
