import unittest

import board
from board import Board
from color import Color
from color import EmptyColor
from coordinate import Coordinate

defined_color = Color('COLOR')
empty_color = EmptyColor()


class TestBoardUtils(unittest.TestCase):
    def test_coordinate_map_to_grid(self):
        coordinate_map = {
            Coordinate(0, 0): defined_color,
            Coordinate(1, 0): defined_color,
            Coordinate(0, 1): empty_color,
        }
        expect_grid = [
            [defined_color, empty_color],
            [defined_color, empty_color],
        ]

        self.assertEqual(board.coordinate_map_to_grid(coordinate_map), expect_grid)
        self.assertEqual(board.coordinate_map_to_grid(None), [])

    def test_grid_to_coordinate_map(self):
        grid = [
            [defined_color, empty_color],
            [defined_color, empty_color],
        ]
        expect_coordinate_map = {
            Coordinate(0, 0): defined_color,
            Coordinate(1, 0): defined_color,
            Coordinate(0, 1): empty_color,
            Coordinate(1, 1): empty_color,
        }

        self.assertEqual(board.grid_to_coordinate_map(grid), expect_coordinate_map)


class TestBoard(unittest.TestCase):
    def test_init(self):
        simple_board = Board([
            [defined_color, empty_color],
            [defined_color, empty_color],
        ])

        self.assertEqual(simple_board.board, [
            [defined_color, empty_color],
            [defined_color, empty_color],
        ])

    def test_from_coordinate_map(self):
        coordinate_map = {
            Coordinate(0, 0): defined_color,
            Coordinate(1, 0): defined_color,
            Coordinate(0, 1): empty_color,
        }

        instance = Board.from_coordinate_map(coordinate_map)
        self.assertEqual(instance.board, [
            [defined_color, empty_color],
            [defined_color, empty_color],
        ])

    def test_from_grid(self):
        grid = [
            [defined_color, empty_color],
            [defined_color, empty_color],
        ]

        instance = Board.from_grid(grid)
        self.assertEqual(instance.board, grid)

    def test_is_solved(self):
        self.assertTrue(Board.from_grid([]).is_solved())
        self.assertFalse(Board.from_grid([[]]).is_solved())

    def test_flood_indices(self):
        grid = [
            [empty_color, defined_color, defined_color],
            [defined_color, empty_color, empty_color],
            [defined_color, defined_color, defined_color],
        ]
        instance = Board.from_grid(grid)

        self.assertEqual(
            instance.flood_indices(Coordinate(0, 0)),
            {Coordinate(0, 0)},
        )
        self.assertEqual(
            instance.flood_indices(Coordinate(0, 1)),
            {Coordinate(0, 1), Coordinate(0, 2)},
        )
        self.assertEqual(
            instance.flood_indices(Coordinate(1, 0)),
            {Coordinate(1, 0), Coordinate(2, 0), Coordinate(2, 1), Coordinate(2, 2)},
        )
        self.assertEqual(
            instance.flood_indices(Coordinate(2, 1)),
            {Coordinate(1, 0), Coordinate(2, 0), Coordinate(2, 1), Coordinate(2, 2)},
        )

    def test_available_moves(self):
        grid = [
            [empty_color, defined_color, defined_color],
            [defined_color, empty_color, empty_color],
            [defined_color, defined_color, defined_color],
        ]
        instance = Board.from_grid(grid)
        available_moves = instance.available_moves()

        for coord, new_board in available_moves:
            self.assertEqual(instance.pop_from(coord), new_board)

    def test_pop_from(self):
        grid = [
            [empty_color, defined_color, defined_color],
            [defined_color, empty_color, empty_color],
            [defined_color, defined_color, defined_color],
        ]
        instance = Board.from_grid(grid)

        self.assertRaises(
            board.InvalidPopException,
            instance.pop_from,
            Coordinate(0, 0),
        )
        self.assertEqual(
            instance.pop_from(Coordinate(0, 2)),
            Board.from_grid([
                [empty_color, empty_color, empty_color],
                [defined_color, empty_color, empty_color],
                [defined_color, defined_color, defined_color],
            ])
        )

    def test_contract(self):
        grid = [
            [empty_color, empty_color, empty_color, defined_color],
            [defined_color, empty_color, defined_color, empty_color],
            [defined_color, empty_color, defined_color, empty_color],
        ]
        instance = Board.from_grid(grid)

        self.assertEqual(
            instance.contract(),
            Board.from_grid([
                [empty_color, empty_color, empty_color],
                [defined_color, defined_color, empty_color],
                [defined_color, defined_color, defined_color],
            ])
        )

    def test_at(self):
        grid = [
            [empty_color, empty_color, empty_color, defined_color],
            [defined_color, empty_color, defined_color, empty_color],
            [defined_color, empty_color, defined_color, empty_color],
        ]
        instance = Board.from_grid(grid)

        self.assertEqual(instance.at(Coordinate(0, 0)), empty_color)
        self.assertEqual(instance.at(Coordinate(1, 0)), defined_color)

    def test_is_coordinate_valid(self):
        grid = [
            [empty_color, empty_color],
            [empty_color, empty_color],
        ]
        instance = Board.from_grid(grid)

        self.assertTrue(instance._is_coordinate_valid(Coordinate(0, 0)))
        self.assertTrue(instance._is_coordinate_valid(Coordinate(0, 1)))
        self.assertTrue(instance._is_coordinate_valid(Coordinate(1, 0)))
        self.assertTrue(instance._is_coordinate_valid(Coordinate(1, 1)))
        self.assertFalse(instance._is_coordinate_valid(Coordinate(2, 2)))
        self.assertFalse(instance._is_coordinate_valid(Coordinate(-1, -1)))

    def test_get_neighbors(self):
        grid = [
            [empty_color, empty_color, empty_color, defined_color],
            [defined_color, empty_color, defined_color, empty_color],
            [defined_color, empty_color, defined_color, empty_color],
        ]
        instance = Board.from_grid(grid)

        self.assertEqual(
            set(instance._get_neighbors(Coordinate(0, 0))),
            {Coordinate(0, 1), Coordinate(1, 0)},
        )
        self.assertEqual(
            set(instance._get_neighbors(Coordinate(1, 1))),
            {Coordinate(0, 1), Coordinate(1, 2), Coordinate(2, 1), Coordinate(1, 0)},
        )

    def test_extract_col(self):
        grid = [
            [empty_color, empty_color, empty_color, defined_color],
            [defined_color, empty_color, defined_color, empty_color],
            [defined_color, empty_color, defined_color, empty_color],
        ]
        instance = Board.from_grid(grid)

        self.assertEqual(
            instance._extract_col(0),
            [empty_color, defined_color, defined_color],
        )
        self.assertEqual(
            instance._extract_col(1),
            [empty_color, empty_color, empty_color],
        )
        self.assertEqual(
            instance._extract_col(2),
            [empty_color, defined_color, defined_color],
        )
        self.assertEqual(
            instance._extract_col(3),
            [defined_color, empty_color, empty_color],
        )

    def test_repr(self):
        grid = [
            [empty_color, empty_color, empty_color, defined_color],
            [defined_color, empty_color, defined_color, empty_color],
            [defined_color, empty_color, defined_color, empty_color],
        ]
        instance = Board.from_grid(grid)

        self.assertEqual(
            repr(instance),
            '----- ----- ----- COLOR\n' +
            'COLOR ----- COLOR -----\n' +
            'COLOR ----- COLOR -----',
        )

    def test_eq(self):
        grid = [
            [empty_color, empty_color, empty_color, defined_color],
            [defined_color, empty_color, defined_color, empty_color],
            [defined_color, empty_color, defined_color, empty_color],
        ]
        instances = [Board.from_grid(grid) for _ in range(5)]

        for one in instances:
            for two in instances:
                self.assertEqual(one, two)
