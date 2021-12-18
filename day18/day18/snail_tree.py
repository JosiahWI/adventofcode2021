from dataclasses import dataclass
import math
from typing import List, Union

@dataclass
class SnailNode:
    parent: "SnailNode" = None
    left: Union["SnailNode", int] = None
    right: Union["SnailNode", int] = None

    def __str__(self) -> str:
        return f"[{self.left}, {self.right}]"

    def add_children_from_pair(self, snail_number) -> None:
        if isinstance(snail_number[0], int):
            self.left = snail_number[0]
        else:
            self.left = SnailNode(parent=self)
            self.left.add_children_from_pair(snail_number[0])

        if isinstance(snail_number[1], int):
            self.right = snail_number[1]
        else:
            self.right = SnailNode(parent=self)
            self.right.add_children_from_pair(snail_number[1])

    @property
    def magnitude(self) -> int:
        if isinstance(self.left, int):
            left = self.left
        else:
            left = self.left.magnitude

        if isinstance(self.right, int):
            right = self.right
        else:
            right = self.right.magnitude

        return 3 * left + 2 * right

    def fix_tree(self) -> bool:
        if self.explode_tree():
            return True
        if self.split_tree():
            return True
        return False

    def explode_tree(self, depth=1) -> bool:
        if depth == 5:
            self.parent.explode_left(self, self.left)
            self.parent.explode_right(self, self.right)
            if self is self.parent.left:
                self.parent.left = 0
            elif self is self.parent.right:
                self.parent.right = 0
            return True
        if isinstance(self.left, SnailNode):
            if self.left.explode_tree(depth + 1):
                return True
        if isinstance(self.right, SnailNode):
            if self.right.explode_tree(depth + 1):
                return True
        return False

    def split_tree(self) -> bool:
        if isinstance(self.left, SnailNode):
            if self.left.split_tree():
                return True
        else:
            if self.left >= 10:
                x, y = self.left // 2, math.ceil(self.left / 2)
                self.left = SnailNode(parent=self)
                self.left.add_children_from_pair([x, y])
                return True
        if isinstance(self.right, SnailNode):
            if self.right.split_tree():
                return True
        else:
            if self.right >= 10:
                x, y = self.right // 2, math.ceil(self.right / 2)
                self.right = SnailNode(parent=self)
                self.right.add_children_from_pair([x, y])
                return True
        return False

    def explode_left(self, child: "SnailNode", value: int) -> None:
        if self.right is child:
            if isinstance(self.left, int):
                self.left += value
            else:
                self.left.add_right(value)
        else:
            if self.parent is None:
                return
            self.parent.explode_left(self, value)

    def explode_right(self, child: "SnailNode", value: int) -> None:
        if self.left is child:
            if isinstance(self.right, int):
                self.right += value
            else:
                self.right.add_left(value)
        else:
            if self.parent is None:
                return
            self.parent.explode_right(self, value)

    def add_left(self, value: int) -> None:
        if isinstance(self.left, int):
            self.left += value
        else:
            self.left.add_left(value)

    def add_right(self, value: int) -> None:
        if isinstance(self.right, int):
            self.right += value
        else:
            self.right.add_right(value)

class SnailTree:

    def __init__(self) -> None:
        self._root = SnailNode()

    def __str__(self) -> str:
        return str(self.root)

    @classmethod
    def from_list(cls, snail_number) -> "SnailTree":
        tree = cls()
        tree.root.add_children_from_pair(snail_number)
        return tree

    @property
    def root(self) -> SnailNode:
        return self._root

    @property
    def magnitude(self) -> int:
        return self._root.magnitude

    def merge(self, other: "SnailTree") -> None:
        self._root = SnailNode(left=self.root, right=other.root)
        self._root.left.parent = self._root
        self._root.right.parent = self._root
        while self._root.fix_tree():
            pass
