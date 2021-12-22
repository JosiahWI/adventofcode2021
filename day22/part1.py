#!/usr/bin/env python3

import re

range_regex = re.compile("(-?[0-9]+)..(-?[0-9]+)")

def from_cuboid(cube_ranges):
    x_range, y_range, z_range = cube_ranges
    # the cuboid range is inclusive, Python's range is not
    for x in range(int(x_range[0]), int(x_range[1]) + 1):
        for y in range(int(y_range[0]), int(y_range[1]) + 1):
            for z in range(int(z_range[0]), int(z_range[1]) + 1):
                yield x, y, z

def cuboid_in_initialization_area(cuboid):
    # we will assume that the cuboid is wholly inside or wholly outside
    vect_3d = from_cuboid(cuboid).__next__()
    return all(component >= -50 and component <= 50 for component in vect_3d)

if __name__ == "__main__":
    import sys
    lines = sys.stdin.readlines()

    activated_cubes = set()
    for line in lines:
        cuboid = range_regex.findall(line)
        if not cuboid_in_initialization_area(cuboid):
            continue

        cubes = set(from_cuboid(cuboid))

        if line[:line.find(" ")] == "on":
            activated_cubes |= cubes
        else:
            activated_cubes -= cubes

    print(f"Part 1: {len(activated_cubes)}")
