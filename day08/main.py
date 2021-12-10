#!/usr/bin/env python3

import itertools
import pathlib

seven_bar_values = {
    "abcefg" : "0",
    "cf" : "1",
    "acdeg" : "2",
    "acdfg" : "3",
    "bcdf" : "4",
    "abdfg" : "5",
    "abdefg" : "6",
    "acf" : "7",
    "abcdefg" : "8",
    "abcdfg" : "9"
}

def replace_all(bar_pattern, replacement_pattern):
    replacement_map = dict(zip(replacement_pattern, "abcdefg"))
    return (replacement_map[val] for val in bar_pattern)

def get_value_by_replacement(*args):
    return seven_bar_values["".join(sorted(replace_all(*args)))]

def match_input_ordering(sample_values):
    for replacement in itertools.permutations("abcdefg"):
        try:
            for pattern in sample_values:
                value = get_value_by_replacement(pattern, replacement)
        except KeyError:
            continue

        # no error was found; it must be valid
        return replacement

def to_display_case(display_string):
    return [s.strip().split(" ") for s in display_string.split("|")]

def find_numeric_value(sample_values, output_values):
    order = match_input_ordering(sample_values)
    assert(order is not None)
    value = "".join(get_value_by_replacement(d, order) for d in output_values)
    return int(value)

if __name__ == "__main__":
    with open(pathlib.Path(__file__).parent / "input.txt", "r") as fp:
        displays = [to_display_case(l.strip()) for l in fp]

    total = sum(find_numeric_value(*d) for d in displays)
    print(f"Part 2: {total}")
