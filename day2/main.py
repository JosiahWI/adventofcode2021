#!/usr/bin/env python3

from dataclasses import dataclass

@dataclass
class Submarine:
    """
    Class to represent a submarine's position and aim.
    """
    x: int = 0
    y: int = 0
    aim: int = 0

    def move(self, direction: str, distance: int) -> None:
        """
        Move the submarine without aim.

        :param direction: Direction to move the submarine. Possible values are:
                "Forward" move the submarine along the x axis.
                "Down" move the submarine along the increasing y axis.
                "Up" move the submarine along the decreasing y axis.

        :param distance: Distance to move along the specified axis.
        """
        if direction == "Forward":
            self.x += distance
        elif direction == "Down":
            self.y += distance
        elif direction == "Up":
            self.y -= distance
        else:
            raise ValueError(f"{direction} is not a valid movement direction.")

    def move_with_aim(self, direction: str, distance: int) -> None:
        """
        Move the submarine with aim.

        :param direction: Direction to move the submarine. Possible values are:
                "Forward" move the submarine along its slope.
                "Down" tilt the submarine towards the increasing y axis.
                "Up" tilt the submarine towards the decreasing y axis.

        :param distance: Distance to move along the slope.
        """
        if direction == "Forward":
            self.x += distance
            self.y += distance * self.aim
        elif direction == "Down":
            self.aim += distance
        elif direction == "Up":
            self.aim -= distance
        else:
            raise ValueError("f{direction} is not a valid movement direction.")

class FormatError(Exception):
    pass

if __name__ == "__main__":
    with open("input.txt", "r") as fp:
        # this could leave empty pairs in the list.
        moves = [line.strip().split() for line in fp.readlines()]

    # now that I mentioned this I can't ignore it
    if moves[-1] == []:
        raise FormatError("Remove the empty lines from your input, bud.")

    # part 1
    sub1 = Submarine()
    for direction, distance in moves:
        sub1.move(direction, int(distance))
    print(f"Part 1: {sub1.x * sub1.y}")

    # part 2
    sub2 = Submarine()
    for direction, distance in moves:
        sub2.move_with_aim(direction, int(distance))
    print(f"Part 2: {sub2.x * sub2.y}")

