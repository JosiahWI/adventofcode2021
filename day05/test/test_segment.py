import unittest

from main import Segment

class TestSegment(unittest.TestCase):

    def test_segment_is_point_raises_value_error(self):
        with self.assertRaises(ValueError):
            Segment((4, 4), (4, 4))

    def test_slope_deltas_with_vertical_segment(self):
        vertical = Segment((0, 1), (0, 5))
        self.assertEqual(vertical.slope_deltas, (0, 1))

    def test_slope_deltas_with_horizontal_segment(self):
        horizontal = Segment((5, 0), (8, 0))
        self.assertEqual(horizontal.slope_deltas, (1, 0))

    def test_forty_five_degree_slope_toward_third_quadrant(self):
        diagonal = Segment((6, 8), (2, 4))
        self.assertEqual(diagonal.slope_deltas, (-1, -1))

    def test_forty_five_degree_slope_toward_fourth_quadrant(self):
        diagonal = Segment((1, 6), (4, 3))
        self.assertEqual(diagonal.slope_deltas, (1, -1))

    def test_integer_points_with_float_step_raises_value_error(self):
        diagonal = Segment((0, 0), (3, 7))
        with self.assertRaises(ValueError):
            diagonal.integer_points()

    def test_integer_points_on_vertical_segment(self):
        vertical = Segment((2, 7), (2, 1))
        expected = [(2, 7), (2, 6), (2, 5), (2, 4), (2, 3), (2, 2), (2, 1)]
        self.assertEqual(list(vertical.integer_points()), expected)

    def test_integer_points_on_horizontal_segment(self):
        horizontal = Segment((0, 5), (3, 5))
        expected = [(0, 5), (1, 5), (2, 5), (3, 5)]
        self.assertEqual(list(horizontal.integer_points()), expected)

    def test_integer_points_on_slope_towards_second_quadrant(self):
        diagonal = Segment((4, 4), (0, 8))
        expected = [(4, 4), (3, 5), (2, 6), (1, 7), (0, 8)]
        self.assertEqual(list(diagonal.integer_points()), expected)
