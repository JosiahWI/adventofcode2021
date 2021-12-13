from .fold import FoldCoords

import pygame

import sys

folder = FoldCoords.from_input(sys.stdin)

def do_fold(line):
    fold = line.split(" ")[-1]
    axis, pos = fold.split("=")
    if axis == "x":
        folder.fold_all(x=int(pos))
    elif axis == "y":
        folder.fold_all(y=int(pos))

# first fold
do_fold(sys.stdin.readline())
print(f"Part 1: {len(folder.coords)}")

# fold all the rest
for line in sys.stdin:
    do_fold(line)

pygame.init()
screen = pygame.display.set_mode((400, 400))

def draw_spot(coord):
    pygame.draw.rect(screen, (0, 0, 0), (coord.x * 4, coord.y * 4, 4, 4))

screen.fill((255, 255, 255))
for coord in folder.coords:
    draw_spot(coord)

pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
