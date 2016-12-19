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
from test.fixtures.three_color_board import three_color_board


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

    def test_load_board(self):
        fixture_path = os.path.join(os.path.dirname(__file__), '../fixtures/3-colors.png')
        board = solve.load_board(fixture_path)
        self.assertEqual(board, three_color_board)

    def test_simulate_touch_events(self):
        solution = (Coordinate(0, 0),)
        with mock.patch.object(subprocess, 'call') as mock_subprocess, suppress_stdout():
            solve.simulate_touch_events(solution)
            mock_subprocess.assert_any_call(['adb', 'shell', 'input', 'tap', '70', '625'])
            mock_subprocess.assert_any_call(['sleep', '1.2'])

    def test_solve_valid(self):
        mock_solution = Solution((Coordinate(0, 0),))
        patch = mock.patch.object

        with patch(solve, 'load_board') as mock_load_board, \
                patch(solve, 'parallel_solve', return_value=mock_solution) as mock_parallel_solve, \
                patch(solve, 'simulate_touch_events') as mock_simulate_touch_events, \
                patch(sys, 'exit') as mock_exit, \
                suppress_stdout():
            solve.solve('file name')

            mock_load_board.assert_called_with('file name')
            self.assertEqual(mock_parallel_solve.call_count, 1)
            self.assertEqual(mock_exit.call_count, 0)
            mock_simulate_touch_events.assert_called_with((Coordinate(0, 0),))

    def test_solve_unsolvable(self):
        mock_solution = EmptySolution()
        patch = mock.patch.object

        with patch(solve, 'load_board') as mock_load_board, \
                patch(solve, 'parallel_solve', return_value=mock_solution) as mock_parallel_solve, \
                patch(solve, 'simulate_touch_events') as mock_simulate_touch_events, \
                patch(sys, 'exit') as mock_exit, \
                suppress_stdout():
            solve.solve('file name')

            mock_load_board.assert_called_with('file name')
            self.assertEqual(mock_parallel_solve.call_count, 1)
            self.assertEqual(mock_exit.call_count, 1)
            self.assertEqual(mock_simulate_touch_events.call_count, 0)

    def test_main_insufficient_args(self):
        sys.argv = []
        with mock.patch.object(sys, 'exit') as mock_exit, \
                mock.patch.object(solve, 'solve') as mock_solve, \
                suppress_stdout():
            solve.main()

            mock_exit.assert_called_with(1)
            self.assertEqual(mock_solve.call_count, 0)

    def test_main_valid_args(self):
        sys.argv = ['python', 'file']
        with mock.patch.object(sys, 'exit') as mock_exit, \
                mock.patch.object(solve, 'solve') as mock_solve, \
                suppress_stdout():
            solve.main()

            self.assertEqual(mock_exit.call_count, 0)
            mock_solve.assert_called_with('file')
