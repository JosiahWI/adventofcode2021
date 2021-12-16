from typing import Iterator, List, Optional

from .packet import Packet, LiteralPacket, OperatorPacket
from .stream import Stream

class OpStack:

    def __init__(self, stream: Stream) -> None:
        self._stream = stream
        self._stack: List[Packet] = []
        self._decode()

    def __str__(self) -> str:
        return str(self._stack)

    def __iter__(self) -> Iterator:
        return iter(self._stack)

    def __getitem__(self, i: int) -> Packet:
        return self._stack[i]

    def __len__(self) -> int:
        return len(self._stack)

    def pop(self, i: int) -> Packet:
        return self._stack.pop(i)

    def _decode_value(self) -> Optional[int]:
        res = ""
        while True:
            val = self._stream.read(5)
            if val is None:
                raise RuntimeError("Bad stream data.")
            bits = bin(val)[2:].zfill(5)
            res = bits[1:] + res
            if bits[0] == "0":
                break
        return int(res, 2)

    def _decode_packet(self) -> Optional[Packet]:
        version = self._stream.read(3)
        if version is None:
            return None

        type_id = self._stream.read(3)
        if type_id is None:
            raise RuntimeError("Bad stream data.")

        if type_id == 4:
            value = self._decode_value()
            if value is None:
                raise RuntimeError("Bad stream data.")
            self._stack.append(LiteralPacket(version, type_id, value))
            return self._stack[-1]
        else:
            length_type_id = self._stream.read(1)
            if length_type_id is None:
                raise RuntimeError("Bad stream data.")
            op = OperatorPacket(version, type_id, length_type_id)
            self._stack.append(op)
            if length_type_id == 0:
                bit_length = self._stream.read(15)
                if bit_length is None:
                    raise RuntimeError("Bad stream data.")
                ptr = self._stream.tell()
                if ptr is None:
                    raise RuntimeError("Bad stream data.")
                stop = ptr + bit_length
                pk_count = 0
                while True:
                    if self._decode_packet() is None:
                        return None
                    pk_count += 1
                    pos = self._stream.tell()
                    if pos is None:
                        break
                    elif pos == stop:
                        break
                    elif pos > stop:
                        raise RuntimeError("Read too much.")
                op.packet_count = pk_count
                    
            elif length_type_id == 1:
                packet_count = self._stream.read(11)
                if packet_count is None:
                    raise RuntimeError("Bad stream data.")
                op.packet_count = packet_count
                for _ in range(packet_count):
                    self._decode_packet()

            return op
        
    def _decode(self) -> None:
        self._decode_packet()
                
