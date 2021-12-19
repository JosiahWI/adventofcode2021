from collections import defaultdict
import itertools
import json
import sys

import pygame

pygame.init()
X_SIZE, Y_SIZE = SCREEN_SIZE = (1000, 1000)
screen = pygame.display.set_mode(SCREEN_SIZE)

def scale(x, y, z):
    # y axis is flipped
    x, y, z = x + 4000,  (-1 * y) + 2200, z + 4000
    return x // 8, y // 8, z // 8

def draw_beacon(color, beacon, depth=True):
    x, y, z = scale(*beacon)
    if depth and z > 0 and z < 4000:
        color = [int(z * (255 / 2000)) if rgb > 0 else 0 for rgb in color]
    pygame.draw.rect(screen, color, (x, y, 4, 4))

def draw_beacons(color, beacons, depth=True):
    for beacon in beacons:
        draw_beacon(color, beacon, depth)

def squared_distance(beacon1, beacon2):
        x1, y1, z1 = beacon1
        x2, y2, z2 = beacon2
        x_diff, y_diff, z_diff = x2 - x1, y2 - y1, z2 - z1
        return x_diff ** 2 + y_diff ** 2 + z_diff ** 2

def distance_pairs(beacons1, beacons2):
    distances = defaultdict(list)
    for pair in itertools.combinations(beacons1, 2):
        distances[squared_distance(*pair)].append(pair)
    for pair in itertools.combinations(beacons2, 2):
        distances[squared_distance(*pair)].append(pair)
    matches = []
    for pairs in distances.values():
        if len(pairs) > 1:
            for pair in pairs:
                matches.extend(pair)
    return matches

scanners = []
deltas = []
for line in sys.stdin:
    if "scanner" in line:
        continue
    elif line == "\n":
        scanners.append(deltas)
        deltas = []
    else:
        deltas.append([int(n) for n in line.split(",")])

def get_nearest(x, y, beacons):
    # get nearest beacon to a point by pythagorean distance
    def dist(beacon):
        x_beacon, y_beacon, _ = scale(*beacon)
        x_diff, y_diff = x - x_beacon, y - y_beacon
        return x_diff ** 2 + y_diff ** 2
    return min(beacons, key=dist)

in_progress = (1, scanners[1])
compare = (1, scanners[0])
select1 = None
select2 = None
hide_others = True
show_depth = False
done = False
highlights = []
while not done:
    screen.fill((255, 255, 255))
    i, beacons = in_progress
    j, compare_beacons= compare
    
    draw_beacons((255, 0, 0), scanners[0], show_depth)
    if not hide_others:
        for other_beacons in scanners[1:]:
            if other_beacons is not beacons:
                draw_beacons((0, 0, 255), other_beacons, show_depth)
        
    draw_beacons((0, 255, 0), beacons, show_depth)
    if select1 is not None:
        draw_beacon((255, 0, 255), select1, depth=False)

    if highlights:
        draw_beacons((0, 0, 255), compare_beacons, show_depth)
    for highlight in highlights:
        draw_beacon((0, 255, 255), highlight, depth=False)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN:
                pygame.quit()
                done = True
                break
            elif event.key == pygame.K_SPACE:
                hide_others = not hide_others
            elif event.key == pygame.K_d:
                show_depth = not show_depth
            elif event.key == pygame.K_RIGHT:
                # cycle scanners to the right
                if i < len(scanners) - 1:
                    in_progress = (i + 1, scanners[i + 1])
            elif event.key == pygame.K_LEFT:
                # cycle scanners to the left
                if i > 1:
                    in_progress = (i - 1, scanners[i - 1])
            elif event.key == pygame.K_n:
                # cycle compare to the right
                if j < len(scanners) - 1:
                    compare = (j + 1, scanners[j + 1])
            elif event.key == pygame.K_p:
                # cycle compare to the left
                if j > 0:
                    compare = (j - 1, scanners[j - 1])
            elif event.key == pygame.K_x:
                # rotate around x axis
                for beacon in beacons:
                    beacon[1], beacon[2] = beacon[2], -beacon[1]
            elif event.key == pygame.K_y:
                # rotate around y axis
                for beacon in beacons:
                    beacon[0], beacon[2] = beacon[2], -beacon[0]
            elif event.key == pygame.K_z:
                # rotate around z axis
                for beacon in beacons:
                    beacon[0], beacon[1] = beacon[1], -beacon[0]
            elif event.key == pygame.K_f:
                # f[ind] highlights pairs with equal distances
                if highlights:
                    highlights = []
                else:
                    highlights = distance_pairs(compare_beacons, beacons)
            elif event.key == pygame.K_s:
                with open("save.json", "w") as fp:
                    json.dump(scanners, fp)
            elif event.key == pygame.K_l:
                with open("save.json", "r") as fp:
                    scanners = json.load(fp)
                    in_progress = (1, scanners[1])

        elif event.type == pygame.MOUSEBUTTONUP:
            if select1 is None:
                select1 = get_nearest(*event.pos, beacons)
            else:
                if highlights:
                    select2 = get_nearest(*event.pos, compare_beacons)
                else:
                    select2 = get_nearest(*event.pos, scanners[0])
                delta = [select2[i] - select1[i] for i in range(3)]
                for beacon in beacons:
                    beacon[0] += delta[0]
                    beacon[1] += delta[1]
                    beacon[2] += delta[2]
                select1, select2 = None, None

unique = set()
for beacons in scanners:
    for beacon in beacons:
        unique.add(tuple(beacon))

print(f"Part 1: {len(unique)}")

def manhattan(a, b):
    return sum(abs(a[i] - b[i]) for i in range(3))

print("Part 2:")
print(f"{max(manhattan(a, b) for a, b in itertools.combinations(unique, 2))}")
