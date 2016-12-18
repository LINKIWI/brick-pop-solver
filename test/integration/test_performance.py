import unittest

import numpy

import util
from solve import load_board
from solve import parallel_solve
from solve import serial_solve

three_board = load_board(util.fixture_path('3-colors.png'))
four_board = load_board(util.fixture_path('4-colors.png'))
five_board = load_board(util.fixture_path('5-colors.png'))
six_board = load_board(util.fixture_path('6-colors.png'))


class TestSerialPerformance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print ''
        print '============SERIAL SOLVER PERFORMANCE BENCHMARK============'

    def test_three_colors(self):
        self.run_test(three_board, 'three colors')

    def run_test(self, board, description, iterations=10):
        print ''
        print 'Executing serial solver {iterations} times ({description})'.format(
            iterations=iterations,
            description=description,
        )

        serial_durations = []
        for _ in range(iterations):
            serial_solution, serial_duration = util.time_func(serial_solve, board)
            self.assertTrue(util.is_solution_valid(board, serial_solution.get_steps()))
            serial_durations.append(serial_duration)
            print 'Serial duration ({description}): {duration} seconds'.format(
                description=description,
                duration=serial_duration,
            )

        print 'Average duration ({description}): {duration} seconds'.format(
            description=description,
            duration=numpy.mean(serial_durations),
        )
        print 'Standard deviation ({description}): {stdev} seconds'.format(
            description=description,
            stdev=numpy.std(serial_durations),
        )


class TestParallelPerformance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print ''
        print '============PARALLEL SOLVER PERFORMANCE BENCHMARK============'

    def test_three_colors(self):
        self.run_test(three_board, 'three colors')

    def test_four_colors(self):
        self.run_test(four_board, 'four colors')

    def test_five_colors(self):
        self.run_test(five_board, 'five colors')

    def test_six_colors(self):
        self.run_test(six_board, 'six colors')

    def run_test(self, board, description, iterations=10):
        print ''
        print 'Executing parallel solver {iterations} times ({description})'.format(
            iterations=iterations,
            description=description,
        )

        parallel_durations = []
        for _ in range(iterations):
            parallel_solution, parallel_duration = util.time_func(parallel_solve, board)
            self.assertTrue(util.is_solution_valid(board, parallel_solution.get_steps()))
            parallel_durations.append(parallel_duration)
            print 'Parallel duration ({description}): {duration} seconds'.format(
                description=description,
                duration=parallel_duration,
            )

        print 'Average duration ({description}): {duration} seconds'.format(
            description=description,
            duration=numpy.mean(parallel_durations),
        )
        print 'Standard deviation ({description}): {stdev} seconds'.format(
            description=description,
            stdev=numpy.std(parallel_durations),
        )
