#!/usr/bin/env python3

import pathlib

def solution_bracket(numbers):
    # assumed numbers are sorted
    end = len(numbers) - 1
    if len(numbers) % 2 == 0:
        return numbers[end // 2], numbers[end // 2 + 1]
    else:
        return numbers[end // 2], numbers[end // 2]

def average(numbers):
    return sum(numbers) // len(numbers)

def cost(pos1, pos2):
    diff = abs(pos1 - pos2)
    return sum(range(1, diff + 1))

if __name__ == "__main__":
    with open(pathlib.Path(__file__).parent / "input.txt", "r") as fp:
        positions = sorted(map(int, fp.readline().split(",")))

    answers = solution_bracket(positions)
    if answers[1] - answers[0] > 0:
        raise ValueError("More than one answer! xD")

    # we will pick the biggest end of the bracket, because bigger is better
    wrong_best_position = answers[1]
    print(f"Part 1: {sum(abs(wrong_best_position - pos) for pos in positions)}")
    best_position = average(positions)
    print(f"Part 2: {sum(cost(best_position, pos) for pos in positions)}")
