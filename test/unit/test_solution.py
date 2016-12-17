import unittest

from solution import Solution
from solution import EmptySolution
from solution import EmptySolutionException

defined_solution = Solution((1, 2, 3))
empty_solution = EmptySolution()


class TestSolution(unittest.TestCase):
    def test_nonempty_init(self):
        self.assertIsNotNone(defined_solution)

    def test_nonempty_is_empty(self):
        self.assertFalse(defined_solution.is_empty())

    def test_nonempty_get_steps(self):
        self.assertEqual(defined_solution.get_steps(), (1, 2, 3))

    def test_nonempty_repr(self):
        self.assertEqual(repr(defined_solution), 'Solution((1, 2, 3))')

    def test_nonempty_str(self):
        self.assertEqual(str(defined_solution), 'Solution((1, 2, 3))')


class TestEmptySolution(unittest.TestCase):
    def test_empty_init(self):
        self.assertIsNotNone(empty_solution)

    def test_empty_is_empty(self):
        self.assertTrue(empty_solution.is_empty())

    def test_empty_get_steps(self):
        self.assertRaises(
            EmptySolutionException,
            empty_solution.get_steps,
        )

    def test_empty_repr(self):
        self.assertEqual(repr(empty_solution), 'EmptySolution()')

    def test_empty_str(self):
        self.assertEqual(str(empty_solution), 'EmptySolution()')
