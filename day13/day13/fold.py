from grid import Coord

class FoldCoords:

    def __init__(self, coords):
        self._coords = coords

    @property
    def coords(self):
        return self._coords

    def fold_all(self, x=None, y=None):
        new_coords = set()
        for coord in self._coords:
            if y is not None:
                if coord.y > y:
                    new_coords.add(coord.reflect(x, y))
                else:
                    new_coords.add(coord)
            elif x is not None:
                if coord.x > x:
                    new_coords.add(coord.reflect(x, y))
                else:
                    new_coords.add(coord)
            else:
                raise ValueError("One of x and y must be positive integers")
        self._coords = new_coords
 
    @classmethod
    def from_input(cls, fp):
        coords = []
        for line in fp:
            # break once we reach the separator
            if line == "\n":
                break
            coords.append(Coord(*[int(c) for c in line.split(",")]))
        return cls(coords)
