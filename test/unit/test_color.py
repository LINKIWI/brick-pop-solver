import unittest

from color import Color
from color import EmptyColor

non_empty = Color('name')
empty = EmptyColor()


class TestColor(unittest.TestCase):
    def test_nonempty_init(self):
        self.assertIsNotNone(non_empty)
        self.assertEqual(non_empty.name, 'name')

    def test_nonempty_is_empty(self):
        # Colors are always considered non-empty
        self.assertFalse(non_empty.is_empty())

    def test_nonempty_eq(self):
        a = Color('a')
        b = Color('b')
        c = Color('a')

        self.assertEqual(a, c)
        self.assertNotEqual(a, b)
        self.assertNotEqual(b, c)

    def test_nonempty_repr(self):
        self.assertEqual(repr(non_empty), 'name')

    def test_nonempty_str(self):
        self.assertEqual(str(non_empty), 'name')

    def test_nonempty_cmp(self):
        a = Color('a')
        b = Color('b')

        self.assertLess(a, b)
        self.assertGreater(b, a)

    def test_nonempty_hash(self):
        self.assertEqual(hash(non_empty), hash('name'))

    def test_nonempty_len(self):
        self.assertEqual(len(non_empty), 4)


class TestEmptyColor(unittest.TestCase):
    def test_empty_init(self):
        self.assertIsNotNone(empty)
        self.assertEqual(empty.name, 'EMPTY')

    def test_empty_is_empty(self):
        # EmptyColors are always considered empty
        self.assertTrue(empty.is_empty())

    def test_empty_eq(self):
        a = EmptyColor()
        b = EmptyColor()

        self.assertEqual(a, b)

    def test_empty_repr(self):
        self.assertEqual(repr(empty), 'EMPTY')

    def test_empty_str(self):
        self.assertEqual(str(empty), 'EMPTY')

    def test_empty_hash(self):
        self.assertEqual(hash(empty), hash('EMPTY'))

    def test_empty_len(self):
        self.assertEqual(len(empty), 5)
