import unittest

from day17 import Probe, Vector

class TestFindParabola(unittest.TestCase):

    def test_after(self):
        probe = Probe(7, 2)
        self.assertEqual(probe.after(7), Vector(28, -7))

    def test_negative_x_velocity(self):
        probe = Probe(-7, 2)
        self.assertEqual(probe.after(7), Vector(-28, -7))

    def test_x_velocity_stops_at_zero(self):
        probe = Probe(1, 0)
        self.assertEqual(probe.after(4), Vector(1, -6))
