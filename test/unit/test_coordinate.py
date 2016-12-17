import unittest

from coordinate import Coordinate

coord = Coordinate(1, 3)


class TestCoordinate(unittest.TestCase):
    def test_init(self):
        self.assertEqual(coord.i, 1)
        self.assertEqual(coord.j, 3)

    def test_offset(self):
        offset = coord.offset(2, -1)
        self.assertEqual(offset.i, 3)
        self.assertEqual(offset.j, 2)

    def test_eq(self):
        a = Coordinate(0, 0)
        b = Coordinate(1, 2)
        c = Coordinate(0, 0)

        self.assertEqual(a, c)
        self.assertNotEqual(a, b)
        self.assertNotEqual(b, c)

    def test_repr(self):
        self.assertEqual(repr(coord), '(1, 3)')

    def test_str(self):
        self.assertEqual(str(coord), '(1, 3)')

    def test_cmp(self):
        self.assertEqual(cmp(Coordinate(0, 0), Coordinate(1, 1)), -1)
        self.assertEqual(cmp(Coordinate(0, 0), Coordinate(0, 1)), -1)
        self.assertEqual(cmp(Coordinate(0, 0), Coordinate(0, 0)), 0)
        self.assertEqual(cmp(Coordinate(0, 0), Coordinate(-1, 0)), 1)
        self.assertEqual(cmp(Coordinate(0, 0), Coordinate(0, -1)), 1)

    def test_hash(self):
        expect = (1 * 0x1f1f1f1f) ^ 3
        self.assertEqual(hash(coord), expect)
