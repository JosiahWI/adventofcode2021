import json
import itertools
import sys

from .snail_tree import SnailNode, SnailTree

lines = [json.loads(line) for line in sys.stdin]
tree = SnailTree.from_list(lines[0])
for line in lines[1:]:
    sub_tree = SnailTree.from_list(line)
    tree.merge(sub_tree)

print(f"Part 1: {tree.magnitude}.")

best_magnitude = -1
for first, second in itertools.permutations(lines, 2):
    tree1, tree2 = SnailTree.from_list(first), SnailTree.from_list(second)
    tree1.merge(tree2)
    magnitude = tree1.magnitude
    if magnitude > best_magnitude:
        best_magnitude = magnitude

print(f"Part 2: {best_magnitude}")
