import sys

from .trench_map import TrenchMap

trenches = TrenchMap.from_input(sys.stdin)

for _ in range(2):
    trenches.enhance()
print(f"Part 1: {trenches.pxls_lit}")

for _ in range(48):
    trenches.enhance()
print(f"Part 2: {trenches.pxls_lit}")
