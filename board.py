from color import EmptyColor
from coordinate import Coordinate
from collections import deque


def coordinate_map_to_grid(coordinate_map):
    if not coordinate_map:
        return []

    max_row = max(map(lambda coord: coord.i, coordinate_map.keys()))
    max_col = max(map(lambda coord: coord.j, coordinate_map.keys()))

    return [
        [
            coordinate_map.get(Coordinate(i, j), EmptyColor())
            for j in range(max_col + 1)
        ]
        for i in range(max_row + 1)
    ]


def grid_to_coordinate_map(grid):
    return {
        Coordinate(i, j): grid[i][j]
        for i in range(len(grid))
        for j in range(len(grid[0]))
    }


class Board:
    def __init__(self, coordinate_map):
        self.coordinate_map = coordinate_map
        self.board = coordinate_map_to_grid(coordinate_map)

    @staticmethod
    def from_coordinate_map(coordinate_map):
        return Board.from_grid(coordinate_map_to_grid(coordinate_map))

    @staticmethod
    def from_grid(grid):
        return Board(grid_to_coordinate_map(grid))

    def is_solved(self):
        return not len(self.board)

    def get_neighbors(self, coord):
        neighboring_coordinates = [
            Coordinate(coord.i + i_offset, coord.j + j_offset)
            for i_offset, j_offset in [(-1, 0), (0, 1), (1, 0), (0, -1)]
        ]

        return filter(self.is_coordinate_valid, neighboring_coordinates)

    def flood_indices(self, coord):
        queue = deque([coord])
        flood = set([])

        while len(queue) > 0:
            location = queue.popleft()
            flood.add(location)

            valid_neighbors = filter(
                lambda index: self.at(index) == self.at(coord) and index not in flood,
                self.get_neighbors(location),
            )
            queue.extend(valid_neighbors)

        return flood

    def available_moves(self):
        pools = set([])

        moves = []
        for coord in self.coordinate_map:
            try:
                new_board = self.pop_from(coord)
                if str(new_board) not in pools:
                    pools.add(str(new_board))
                    moves.append((coord, new_board))
            except InvalidPopException:
                pass

        return moves

    def pop_from(self, coord):
        # Get a list of all the indices that can be popped from this location
        to_pop = self.flood_indices(coord)

        # The game forbids popping an index where the flood size is unity
        if len(to_pop) == 1:
            raise InvalidPopException('Unable to pop from a flood group with only one element')

        # Update the coordinate map with a None value for all elements that are to be removed
        update_coordinate_map = {
            pop_index: EmptyColor()
            for pop_index in to_pop
        }

        return Board(dict(self.coordinate_map, **update_coordinate_map)).contract()

    def contract(self):
        return self._contract_cols()._contract_rows()

    def is_coordinate_valid(self, coord):
        return 0 <= coord.i < len(self.board) and 0 <= coord.j < len(self.board[0])

    def at(self, coord):
        return self.board[coord.i][coord.j]

    def _contract_cols(self):
        # Build a map of the number of empty rows in each column
        col_empty_counts = {
            col: len(filter(lambda elem: elem.is_empty(), self._extract_col(col)))
            for col in range(len(self.board[0]))
        }

        # Get a list of all the columns that need to be removed
        to_remove_cols = filter(lambda col: col_empty_counts[col] == len(self.board), col_empty_counts.keys())

        update_grid = [
            [
                col
                for j, col in enumerate(row)
                if j not in to_remove_cols
            ]
            for row in self.board
        ]

        return Board.from_grid(update_grid)

    def _contract_rows(self):
        # For each coordinate, determine the amount by which the index needs to vertically drop
        drop_counts = {
            coord: len(filter(lambda elem: elem.is_empty(), self._extract_col(coord.j)[coord.i:]))
            for coord in self.coordinate_map
            if not self.at(coord).is_empty()
        }

        update_coordinate_map = {
            coord.offset(drop_counts.get(coord, 0), 0): self.at(coord)
            for coord in self.coordinate_map.keys()
            if drop_counts.get(coord, 0) > 0 or not self.at(coord).is_empty()
        }

        return Board(update_coordinate_map)

    def _extract_col(self, col):
        return [
            row[col]
            for row in self.board
        ]

    def __repr__(self):
        try:
            color_length = max(map(len, self.coordinate_map.values()))
        except:
            color_length = 1

        return '\n'.join([
            ' '.join(map(lambda elem: '-' * color_length if elem.is_empty() else str(elem), self.board[row]))
            for row in range(len(self.board))
        ])


class InvalidPopException(Exception):
    pass
