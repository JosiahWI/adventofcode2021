from dataclasses import dataclass
from typing import Tuple

@dataclass(eq=True)
class Vector:
    x: int
    y: int

    def copy(self) -> "Vector":
        return Vector(self.x, self.y)

class Probe:

    def __init__(self, x_velocity: int, y_velocity: int) -> None:
        self._pos = Vector(0, 0)
        self._velocity = Vector(x_velocity, y_velocity)

    @property
    def acceleration(self) -> int:
        y_accel = -1
        if self._velocity.x > 0:
            x_accel = -1
        elif self._velocity.x == 0:
            x_accel = 0
        else:
            x_accel = 1

        return x_accel, y_accel

    @property
    def pos(self) -> Vector:
        return self._pos.copy()

    @property
    def velocity(self) -> Vector:
        return self._velocity.copy()

    def after(self, steps: int) -> Vector:
        for _ in range(steps):
            self._step()
        return self.pos
 
    def step(self) -> None:
        self._pos.x += self._velocity.x
        self._pos.y += self._velocity.y
        x_accel, y_accel = self.acceleration
        self._velocity.x += x_accel
        self._velocity.y += y_accel

def max_height(probe: Probe, target_bounds: Tuple[Tuple[int, int]]) -> int:
    while probe.velocity.y > 0:
        probe.step()
            
    max_height = probe.pos.y

    # we make an assumption that the highest point is before the target area
    while probe.velocity.x > 0 or probe.pos.y > target_bounds[1][1]:
        probe.step()
        pos = probe.pos
        if pos.x >= target_bounds[0][0] \
                and pos.x <= target_bounds[0][1] \
                and pos.y >= target_bounds[1][0] \
                and pos.y <= target_bounds[1][1]:
            return max_height
    raise TargetNotReachedError()

class TargetNotReachedError(Exception):
    pass
