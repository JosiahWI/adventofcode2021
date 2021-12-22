#!/usr/bin/env python3

import re
import time

range_regex = re.compile(r"(-?\d+)..(-?\d+)")

def cubes_in(cuboid):
    x_range, y_range, z_range = cuboid
    return (x_range[1] - x_range[0] + 1) * \
           (y_range[1] - y_range[0] + 1) * \
           (z_range[1] - z_range[0] + 1)

def split_cuboid(active_cuboid, other_cuboid):
    x_on, y_on, z_on = active_cuboid
    x_other, y_other, z_other = other_cuboid
    # if the cuboids do not intersect then there is no change
    if x_other[1] < x_on[0] or x_other[0] > x_on[1] or \
            y_other[1] < y_on[0] or y_other[0] > y_on[1] or \
            z_other[1] < z_on[0] or z_other[0] > z_on[1]:
        return [active_cuboid]

    new_cuboids = []
    if x_other[0] > x_on[0]:
        new_cuboids.append([[x_on[0], x_other[0] - 1], y_on, z_on])
        x_on = [x_other[0], x_on[1]]
    if x_other[1] < x_on[1]:
        new_cuboids.append([[x_other[1] + 1, x_on[1]], y_on, z_on])
        x_on = [x_on[0], x_other[1]]
    if y_other[0] > y_on[0]:
        new_cuboids.append([x_on, [y_on[0], y_other[0] - 1], z_on])
        y_on = [y_other[0], y_on[1]]
    if y_other[1] < y_on[1]:
        new_cuboids.append([x_on, [y_other[1] + 1, y_on[1]], z_on])
        y_on = [y_on[0], y_other[1]]
    if z_other[0] > z_on[0]:
        new_cuboids.append([x_on, y_on, [z_on[0], z_other[0] - 1]])
        z_on = [z_other[0], z_on[1]]
    if z_other[1] < z_on[1]:
        new_cuboids.append([x_on, y_on, [z_other[1] + 1, z_on[1]]])
        z_on = [z_on[0], z_other[1]]
    return new_cuboids

if __name__ == "__main__":
    t_start = time.perf_counter()
    import sys
    lines = sys.stdin.readlines()

    # cuboids that are on
    active_cuboids = []
    for line in lines:
        new_active_cuboids = []
        other_cuboid = [
            [int(x) for x in range_]
            for range_ in range_regex.findall(line)
            ]

        if line[:line.find(" ")] == "on":
            for cuboid in active_cuboids:
                # if two ON cuboids intersect, we would end up doing
                # multiple splits on the same section, and end
                # up with duplicate cuboids and a huge problem.
                # to avoid this we split one of the ON cuboids
                new_active_cuboids.extend(split_cuboid(cuboid, other_cuboid))
            new_active_cuboids.append(other_cuboid)

        else:
            for cuboid in active_cuboids:
                new_active_cuboids.extend(split_cuboid(cuboid, other_cuboid))

        active_cuboids = new_active_cuboids

print(f"Part 2: {sum(cubes_in(cuboid) for cuboid in active_cuboids)}")
t_stop = time.perf_counter()
print(f"Time elapsed: {t_stop - t_start}")
