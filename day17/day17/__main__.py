import re
import sys

from .find_parabola import Probe, max_height, TargetNotReachedError

target_regex = re.compile("(-?[0-9]+)\.\.(-?[0-9]+)")

str_target_bounds = target_regex.findall(sys.stdin.readline())
target_bounds = [sorted([int(x) for x in bound]) for bound in str_target_bounds]

result = None
valid_velocities = 0
for x in range(1, 500):
    for y in range(-200, 200):
        try:
            highest = max_height(Probe(x, y), target_bounds)
        except TargetNotReachedError:
            continue

        valid_velocities += 1
        if result is None or highest > result:
            result = highest

print(f"Part 1: {result}")
print(f"Part 2: {valid_velocities}")
