import math
import sys
from typing import List

from .op_stack import OpStack
from .packet import Packet, LiteralPacket, OperatorPacket
from .stream import Stream

stream = Stream(sys.stdin.read().strip())

stack = OpStack(stream)

print(f"Part 1: {sum(packet.version for packet in stack)}")

operands: List[int] = []
while len(stack) > 0:
    packet = stack.pop(-1)
    if isinstance(packet, LiteralPacket):
        operands.append(packet.value)
    elif isinstance(packet, OperatorPacket):
        if packet.type_id == 0:
            temp = [operands.pop(-1) for _ in range(packet.packet_count)]
            operands.append(sum(temp))
        elif packet.type_id == 1:
            temp = [operands.pop(-1) for _ in range(packet.packet_count)]
            operands.append(math.prod(temp))
        elif packet.type_id == 2:
            temp = [operands.pop(-1) for _ in range(packet.packet_count)]
            operands.append(min(temp))
        elif packet.type_id == 3:
            temp = [operands.pop(-1) for _ in range(packet.packet_count)]
            operands.append(max(temp))
        elif packet.type_id == 5:
            if len(operands) < 2:
                raise RuntimeError("Wrong number of operands on stack.")
            operands.append(1 if operands.pop(-1) > operands.pop(-1) else 0)
        elif packet.type_id == 6:
            if len(operands) < 2:
                raise RuntimeError("Wrong number of operands on stack.")
            operands.append(1 if operands.pop(-1) < operands.pop(-1) else 0)
        elif packet.type_id == 7:
            if len(operands) < 2:
                raise RuntimeError("Wrong number of operands on stack.")
            operands.append(1 if operands.pop(-1) == operands.pop(-1) else 0)
    #print(f"{packet} -> {operands}")

if len(operands) > 1:
    raise RuntimeError("Too many operands left over!!")

print(f"Part 2: {operands[0]}")
