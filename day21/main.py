#!/usr/bin/env python3

# part 2

from collections import defaultdict
import functools

frequency = defaultdict(int)
for i in range(1, 4):
    for j in range(1, 4):
        for k in range(1, 4):
            total = i + j + k
            frequency[total] += 1

def move(old_pos, squares):
    new_pos = (old_pos + squares) % 10
    if new_pos == 0:
        new_pos = 10
    return new_pos 

@functools.cache
def count_wins(pos1, score1, pos2, score2):
    wins1, wins2 = 0, 0
    for outcome in range(3, 10):
        new_pos1 = move(pos1, outcome)
        new_score1 = new_pos1 + score1
        if new_score1 >= 21:
            wins1 += frequency[outcome]
        else:
            for outcome2 in range(3, 10):
                new_pos2 = move(pos2, outcome2)
                new_score2 = new_pos2 + score2
                if new_score2 >= 21:
                    wins2 += frequency[outcome] * frequency[outcome2]
                else:
                    new_wins1, new_wins2 = count_wins(
                        new_pos1, new_score1, new_pos2, new_score2)
                    wins1 += new_wins1 * frequency[outcome] \
                          * frequency[outcome2]
                    wins2 += new_wins2 * frequency[outcome] \
                          * frequency[outcome2]

    return wins1, wins2

if __name__ == "__main__":
    import sys

    pos1 = int(sys.stdin.readline().split(":")[1])
    pos2 = int(sys.stdin.readline().split(":")[1])
    print(f"Part 2: {max(count_wins(pos1, 0, pos2, 0))}")
