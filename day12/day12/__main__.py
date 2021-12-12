from .cave_graph import CaveGraph

import sys

graph = CaveGraph.from_lines(sys.stdin.readlines())

print(f"Part 1: {len(list(graph.all_paths()))}")
print(f"Part 2: {len(list(graph.all_paths(extra_visit=True)))}")
