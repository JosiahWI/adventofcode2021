#!/usr/bin/env python3

import pathlib

class FlashSimulator:

    def __init__(self, grid):
        self._grid = grid
        self._flashes_queued = set()
        self._already_flashed = set()

    def __str__(self):
        return '\n'.join([''.join(map(str, row)) for row in self._grid]) + '\n'

    @property
    def grid(self):
        return self._grid

    @classmethod
    def from_input(cls, fp):
        return cls([[int(x) for x in row.strip()] for row in fp])

    def adjacent(self, x, y):
        """
        Positions adjacent to (x, y), including diagonals.
        """
        offsets = {(1, 0), (1, -1), (0, -1), (-1, -1),
            (-1, 0), (-1, 1), (0, 1), (1, 1)}
        for offset in offsets:
            try:
                check_pos = (x + offset[0], y + offset[1])
                # quick check because I am in a hurry
                if check_pos[0] < 0 or check_pos[1] < 0:
                    continue
                if self._grid[check_pos[1]][check_pos[0]]:
                    yield check_pos
            except IndexError:
                continue

    def inc_all(self):
        for y, row in enumerate(self._grid):
            for x, _ in enumerate(row):
                self.inc(x, y)
        self.add_flashes()

    def add_flashes(self):
        for y, row in enumerate(self._grid):
            for x, energy in enumerate(row):
                if energy > 9:
                    self._flashes_queued.add((x, y))

    def flash(self, x, y):
        self._grid[y][x] = 0
        self._already_flashed.add((x, y))
        for x_adj, y_adj in self.adjacent(x, y):
            self.inc(x_adj, y_adj)

    def inc(self, x, y):
        if not (x, y) in self._already_flashed:
            self._grid[y][x] += 1

    def apply(self):
        """
        Applies all queued changes, and may queue more changes in the process.
        """
        flashes = 0
        while self._flashes_queued:
            for x, y in self._flashes_queued:
                self.flash(x, y)
                flashes += 1
            self._flashes_queued = set()
            self.add_flashes()

        self._already_flashed = set()
        return flashes

if __name__ == "__main__":
    with open(pathlib.Path(__file__).parent / "input.txt", "r") as fp:
        flashes = FlashSimulator.from_input(fp)

    total = 0
    for _ in range(100):
        flashes.inc_all()
        total += flashes.apply()
        print(flashes)

    iters = 100
    while True:
        iters += 1
        flashes.inc_all()
        how_many = flashes.apply()
        if how_many == 100:
            break

    print(f"Part 1: {total}")
    print(f"Part 2: {iters}")
