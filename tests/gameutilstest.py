import unittest
from unittest.mock import MagicMock


from gameutils import GameMath


class TestMethod(unittest.TestCase):

    def test_get_direction(self):
        self.assertEqual((1, 1),GameMath.get_direction(1, 1))
        self.assertEqual((0, -1),GameMath.get_direction(0, -5))
        self.assertEqual((-1, 0),GameMath.get_direction(-5, -2))
        self.assertEqual((1, 0),GameMath.get_direction(5, 2))
