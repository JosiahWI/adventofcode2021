from dataclasses import dataclass
from typing import List

@dataclass()
class Packet:
    version: int
    type_id: int

@dataclass()
class LiteralPacket(Packet):
    value: int

@dataclass()
class OperatorPacket(Packet):
    length_type_id: int
    packet_count: int = 0
