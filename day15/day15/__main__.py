from .cost_tree import make_cost_tree

from grid import Coord, Grid

import sys

def extend_right(row, width, i):
    new_row = [x + i for x in row[:width]]
    new_row = [x - 9 if x > 9 else x for x in new_row]
    row.extend(new_row)

def extend_down(rows, height, i):
    new_rows = []
    for row in rows[:height]:
        new_row = [x + i for x in row]
        new_row = [x - 9 if x > 9 else x for x in new_row]
        new_rows.append(new_row)
    rows.extend(new_rows)

raw_grid = [[int(x) for x in row.strip()] for row in sys.stdin]
grid = Grid(raw_grid)
target = Coord(grid.width - 1, grid.height - 1)
cost_tree = make_cost_tree(grid, Coord(0, 0))
print(f"Part 1: {cost_tree[target][1]}")

# hehe, modifies grid in place

width = grid.width
for row in raw_grid:
    for i in range(1, 5):
        extend_right(row, width, i)

height = grid.height
for i in range(1, 5):
    extend_down(raw_grid, height, i)
cost_tree = make_cost_tree(grid, Coord(0, 0))
target = Coord(grid.width - 1, grid.height - 1)
print(f"Part 2: {cost_tree[target][1]}")
