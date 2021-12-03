#!/usr/bin/env python3

from collections import Counter
import pathlib

class Diagnostic:

    def __init__(self, diagnostics):
        self._bit_graph = diagnostics

    @classmethod
    def from_file(cls, filename):
        with open(f"{pathlib.Path(__file__).parent}/{filename}", "r") as fp:
            return cls([line.strip() for line in fp])

    def copy(self):
        return self.__class__(self._bit_graph[:])

    def col_iter(self, col_index):
        for bits in self._bit_graph:
            yield bits[col_index]

    def most_common_bit(self, col_index, on_tie=None):
        frequency_map = dict(Counter(self.col_iter(col_index)).most_common())
        bin_zeros = frequency_map.get('0', 0)
        bin_ones = frequency_map.get('1', 0)
        if bin_zeros == bin_ones:
            return on_tie
        else:
            return max(frequency_map, key=lambda x: frequency_map.get(x, 0))

    def most_common_bits(self, on_tie=None):
        for i in range(len(self._bit_graph[0])):
            yield self.most_common_bit(i, on_tie)

    def least_common_bit(self, col_index, on_tie=None):
        return '0' if self.most_common_bit(col_index) == '1' else '0'

    def least_common_bits(self, on_tie=None):
        for i in range(len(self._bit_graph[0])):
            yield self.least_common_bit(i, on_tie)

    @property
    def power_consumption(self):
        gamma = int(''.join(self.most_common_bits()), 2)
        # bitwise not would invert the sign
        return gamma * (gamma ^ 0xFFF)

if __name__ == "__main__":
    diagnostic = Diagnostic.from_file("input.txt")
    print(f"Power Consumption is {diagnostic.power_consumption}")
