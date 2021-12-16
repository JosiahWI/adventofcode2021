import unittest

from day16 import Stream

class TestStream(unittest.TestCase):

    def test_read_data_back(self):
        stream = Stream("2A")
        self.assertEqual(stream.read(), 42)

    def test_read_three_bit_segments(self):
        stream = Stream("8A0")
        result = [stream.read(3) for _ in range(4)]
        self.assertListEqual(result, [4, 2, 4, 0])
