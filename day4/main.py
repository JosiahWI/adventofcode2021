#!/usr/bin/env python3

from more_itertools import flatten
import numpy
import pathlib

class Board:

    def __init__(self, grid):
        self._grid = numpy.array(grid)
        self.no_solve = False
        self.solved_on = None

    @classmethod
    def from_chunk_of_text(cls, chunk_of_text):
        lines = [line for line in chunk_of_text.split('\n') if line != '']
        return cls([[int(x) for x in l.split(' ') if x != ''] for l in lines])

    def is_solved(self):
        # thank you to Casca on Discord for the idea of marking by replacement
        if any(all(x == -1 for x in row) for row in self._grid):
            return True
        if any(all(x == -1 for x in col) for col in self._grid.transpose()):
            return True
        return False

    def steps_to_solve(self, guesses):
        steps = 0
        for guess in guesses:
            steps += 1
            for row_i, row in enumerate(self._grid):
                for col_i, number in enumerate(row):
                    if number == guess:
                        self._grid[row_i][col_i] = -1
            if self.is_solved():
                self.solved_on = guess
                return steps
        self.no_solve = True
        return None

    def score(self):
        return sum([n for n in flatten(self._grid) if n != -1]) * self.solved_on

if __name__ == "__main__":
    with open(f"{pathlib.Path(__file__).parent}/input.txt", "r") as fp:
        guesses = [int(guess) for guess in fp.readline().split(',')]
        boards = [Board.from_chunk_of_text(x) for x in fp.read().split("\n\n")]

    boards.sort(key=lambda board: board.steps_to_solve(guesses))
    boards = [board for board in boards if board.no_solve is False]
    print(f"Part 1: {boards[0].score()}")
    print(f"Part 2: {boards[-1].score()}")
