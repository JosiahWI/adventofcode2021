#!/usr/bin/env python3

print((lambda seq: sum(sum(seq[i]) < sum(seq[i + 1]) for i in range(len(seq) - 1)))((lambda seq: [(seq[i], seq[i + 1], seq[i + 2]) for i in range(len(seq) - 3)])([int(l.strip()) for l in open("input.txt", "r").readlines()])))

"""
    print(f"Testing {len(numbers)} numbers.")
    times_increased = 0
    for i, n in enumerate(numbers):
        try:
            prev_sum = numbers[i - 3] + numbers[i - 2] + numbers[i - 1]
            curr_sum = numbers[i - 2] + numbers[i - 1] + n
            if curr_sum > prev_sum:
                times_increased += 1
        except IndexError:
            # throw out the index error where i = 0
            pass

    print(times_increased)
"""
