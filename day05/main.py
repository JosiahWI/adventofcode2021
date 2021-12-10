#!/usr/bin/env python3

from collections import Counter
from more_itertools import flatten
import pathlib

class Segment:

    def __init__(self, pt1, pt2):
        if pt1 == pt2:
            raise ValueError(f"{pt1} and {pt2} are not distinct.")
        self._pt1 = pt1
        self._pt2 = pt2

    @classmethod
    def from_str(cls, pt_str):
        pt_pair = pt_str.split(" -> ")
        points = [[int(pos) for pos in pt.split(",")] for pt in pt_pair]
        return cls(*points)

    @property
    def slope_deltas(self):
        """
        The slope of the line segment as (x, y) deltas.

        x will be 1 or -1, and y will be scaled, except in the special case
        that x is 0.
        """
        x_delta = self._pt2[0] - self._pt1[0]
        y_delta = self._pt2[1] - self._pt1[1]
        # horizontal and verticle lines are both special cases
        # we do not allow constructing a segment where x and y deltas are both 0
        if x_delta == 0:
            return (x_delta, y_delta / abs(y_delta))
        elif y_delta == 0:
            return (x_delta / abs(x_delta), y_delta)
        divisor = abs(x_delta)
        return (x_delta / divisor, y_delta / divisor)

    def integer_points(self):
        """
        Find the integer points on the segment including the endpoints.
        """
        x_step, y_step = self.slope_deltas
        if int(x_step) != x_step or int(y_step) != y_step:
            raise ValueError(f"({x_step}, {y_step}) is not an integer step.")

        # vertical and horizontal lines are once again special cases
        if x_step == 0:
            ys = range(self._pt1[1], self._pt2[1] + int(y_step), int(y_step))
            return ((self._pt1[0], y) for y in ys)
        elif y_step == 0:
            xs = range(self._pt1[0], self._pt2[0] + int(x_step), int(x_step))
            return ((x, self._pt1[1]) for x in xs)
        else:
            return zip(
                range(self._pt1[0], self._pt2[0] + int(x_step), int(x_step)),
                range(self._pt1[1], self._pt2[1] + int(y_step), int(y_step)))

if __name__ == "__main__":
    with open(f"{pathlib.Path(__file__).parent}/input.txt", "r") as fp:
        segment_strs = fp.readlines()

    segments = (Segment.from_str(inp_str) for inp_str in segment_strs)
    segments_as_points = (seg.integer_points() for seg in segments)
    point_frequencies = dict(Counter(flatten(segments_as_points)).most_common())

    print(sum(count > 1 for count in point_frequencies.values()))
