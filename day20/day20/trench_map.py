from collections import defaultdict
from typing import List, Set, Tuple

Image = defaultdict[Tuple[int, int], int]

class TrenchMap:

    def __init__(self, image: Image, enhancement_table: List[int]) -> None:
        self._image: Image = image
        self._enhancement_table = enhancement_table
        self._default_state = 0

    def enhance(self) -> None:
        update_px = set()
        # default state is toggled at the end
        new_image = defaultdict(lambda: self._default_state)
        for coord, _ in self._image.items():
            update_px.add(coord)
            # neighbors come back in the top left to bottom right order
            for x, y in self.neighbors(*coord):
                update_px.add((x, y))

        for coord in update_px:
            new_image[coord] = self.enhance_state(coord)

        self._image = new_image
     
        if self._default_state == 0:
            self._default_state = self._enhancement_table[0]
        else:
            self._default_state = self._enhancement_table[-1]

    def enhance_state(self, coord) -> int:
        px_states = (str(self._image[ngb]) for ngb in self.neighbors(*coord))
        enhancement_index = int("".join(px_states), 2)
        return self._enhancement_table[enhancement_index]

    @property
    def image(self) -> Image:
        return self._image

    @property
    def pxls_lit(self) -> int:
        return sum(self._image.values())

    @classmethod
    def from_input(cls, _input) -> "TrenchMap":
        enhancement_table = list(TrenchMap.pxls_to_ints((_input.readline())))
        # skip empty line
        _input.readline()
        image = defaultdict(int)
        for y, row in enumerate(_input):
            for x, px_state in enumerate(TrenchMap.pxls_to_ints(row)):
                image[(x, y)] = px_state

        return cls(image, enhancement_table)

    @staticmethod
    def pxls_to_ints(pixels: str):
        if not isinstance(pixels, str):
            raise ValueError("Pixel image input must be a string.")
        return (0 if px == '.' else 1 for px in pixels.strip())

    @staticmethod
    def neighbors(x: int, y: int):
        offsets = [(-1, -1), (0, -1), (1, -1),
                   (-1, 0), (0, 0), (1, 0),
                   (-1, 1), (0, 1), (1, 1)]
        for x_off, y_off in offsets:
            yield (x + x_off, y + y_off)
