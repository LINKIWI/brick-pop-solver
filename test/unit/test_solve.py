import os
import subprocess
import sys
import unittest
from contextlib import contextmanager

import mock

import solve
from board import Board
from color import Color
from coordinate import Coordinate
from solution import EmptySolution
from solution import Solution


@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


class TestSolve(unittest.TestCase):
    def test_solution_search_solved(self):
        available_moves = [(Coordinate(0, 0), Board.from_grid([]))]
        mock_queue = mock.MagicMock()
        solve.solution_search(mock_queue, available_moves)
        mock_queue.put.assert_called_once_with(Solution((Coordinate(0, 0),)))

    def test_solution_search_unsolvable(self):
        available_moves = [(Coordinate(0, 0), Board.from_grid([[]]))]
        mock_queue = mock.MagicMock()
        solve.solution_search(mock_queue, available_moves)
        mock_queue.put.assert_called_once_with(EmptySolution())

    def test_solution_search_recursive(self):
        grid = [
            [Color('one'), Color('one')],
            [Color('two'), Color('two')],
        ]
        board = Board.from_grid(grid)

        available_moves = board.available_moves()
        mock_queue = mock.MagicMock()
        solve.solution_search(mock_queue, available_moves)
        mock_queue.put.assert_any_call(Solution((Coordinate(0, 0), Coordinate(1, 0))))

    def test_replay_steps(self):
        board = Board.from_grid([
            [Color('one'), Color('one')],
            [Color('two'), Color('two')],
        ])
        solution_steps = (Coordinate(0, 0), Coordinate(1, 0))

        with mock.patch.object(solve, 'render_step_image') as mock_render_step_image:
            solve.replay_steps(board, solution_steps)
            self.assertEqual(mock_render_step_image.call_count, 2)

    def test_simulate_touch_events(self):
        solution = (Coordinate(0, 0),)
        with mock.patch.object(subprocess, 'call') as mock_subprocess, suppress_stdout():
            solve.simulate_touch_events(solution)
            mock_subprocess.assert_any_call(['adb', 'shell', 'input', 'tap', '70', '625'])
            mock_subprocess.assert_any_call(['sleep', '1.2'])

