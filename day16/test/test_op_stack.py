import unittest

from day16 import OpStack, Stream

class TestOpStack(unittest.TestCase):

    def test_decode_literal_with_extreaneous_zeros(self):
        stream = Stream("3221")
        stack = OpStack(stream)
        self.assertEqual(stack[0].value, 17)
