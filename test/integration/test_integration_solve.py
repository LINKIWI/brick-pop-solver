import os
import time
import unittest

from solve import load_board
from solve import parallel_solve
from solve import solve_board_dfs


cwd = os.path.dirname(__file__)
three_board = load_board(os.path.join(cwd, '../fixtures/3-colors.png'))
four_board = load_board(os.path.join(cwd, '../fixtures/4-colors.png'))
five_board = load_board(os.path.join(cwd, '../fixtures/5-colors.png'))
six_board = load_board(os.path.join(cwd, '../fixtures/6-colors.png'))


def time_func(target, *args, **kwargs):
    """
    Time the execution of a function.

    :param target: The target function.
    :param args: Arguments to the function.
    :param kwargs: Keyword arguments to the function.
    :return: The original return value of args and kwargs applied to the target.
    """
    start_time = time.time()
    ret = target(*args, **kwargs)
    end_time = time.time()
    print 'Function took {duration} seconds'.format(duration=end_time - start_time)
    return ret


def is_solution_valid(board, solution):
    """
    Check if a generated solution is valid for a given board.

    :param board: The original, starting board.
    :param solution: A full solution, i.e. a list of Coordinates.
    :return: True if the solution is valid; False otherwise.
    """
    if not solution:
        return board.is_solved()

    return is_solution_valid(board.pop_from(solution[0]), solution[1:])


class TestIntegrationSerialSolve(unittest.TestCase):
    def test_serial_solve_three_colors(self):
        self.assert_valid_serial_solve(three_board)

    def assert_valid_serial_solve(self, board):
        solution = time_func(solve_board_dfs, board)
        self.assertFalse(solution.is_empty())
        self.assertTrue(is_solution_valid(board, solution.get_steps()))


class TestIntegrationParallelSolve(unittest.TestCase):
    def test_parallel_solve_three_colors(self):
        self.assert_valid_parallel_solve(three_board)

    def test_parallel_solve_four_colors(self):
        self.assert_valid_parallel_solve(four_board)

    def test_parallel_solve_five_colors(self):
        self.assert_valid_parallel_solve(five_board)

    def test_parallel_solve_six_colors(self):
        self.assert_valid_parallel_solve(six_board)

    def assert_valid_parallel_solve(self, board):
        solution = time_func(parallel_solve, board)
        self.assertFalse(solution.is_empty())
        self.assertTrue(is_solution_valid(board, solution.get_steps()))
