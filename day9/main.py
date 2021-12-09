#!/usr/bin/env python3

from more_itertools import flatten

import functools
import pathlib

class LavaCaves:

    def __init__(self, grid):
        self._grid = grid

    @classmethod
    def from_input(cls, fp):
        grid = []
        for row in fp:
            # strip is necessary because the newline won't be ignored
            grid.append([int(x) for x in row.strip()])
        return cls(grid)

    @property
    def local_minimums(self):
        for y, row in enumerate(self._grid):
            for x, height in enumerate(row):
                # every position has at least 1 adjacent
                if height < min(self.height_adjacent((x, y))):
                    yield (x, y), height

    @property
    def basins(self):
        return (self.basin(pos) for pos, _ in self.local_minimums)

    def adjacents_to_pos(self, pos):
        """The values of the points horizontally or vertically adjacent."""
        x, y = pos
        offsets_to_adjacents = [(1, 0), (0, -1), (-1, 0), (0, 1)]
        for x_off, y_off in offsets_to_adjacents:
            x_adj, y_adj = x + x_off, y + y_off
            # the index is only evaluated if the row exists
            if y_adj >= 0 and y_adj < len(self._grid) and \
               x_adj >= 0 and x_adj < len(self._grid[0]):
                yield x_adj, y_adj

    def height_adjacent(self, pos):
        # this could be a problem if the size of the grid could change xD
        # fortunately for Advent of Code this is not too important
        return (self._grid[y][x] for x, y in self.adjacents_to_pos(pos))

    def basin(self, pos):
        in_basin = {pos}
        maybe_in_basin = set(self.adjacents_to_pos(pos))
        while maybe_in_basin:
            new = set()
            for x, y in maybe_in_basin:
                if self._grid[y][x] != 9 and (x, y) not in in_basin:
                    new.add((x, y))
            maybe_in_basin = set(flatten(self.adjacents_to_pos(p) for p in new))
            in_basin |= new
        return in_basin       

def product(iterable):
    return functools.reduce(lambda x, y: x * y, iterable)

if __name__ == "__main__":
    with open(pathlib.Path(__file__).parent / "input.txt", "r") as fp:
        caves = LavaCaves.from_input(fp)

    print(f"Part 1: {sum(height + 1 for _, height in caves.local_minimums)}")

    biggest_basins = sorted(caves.basins, key=len, reverse=True)[0:3]
    print(f"Part 2: {product(len(basin) for basin in biggest_basins)}")
