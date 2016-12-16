from collections import deque

from color import EmptyColor
from coordinate import Coordinate


def coordinate_map_to_grid(coordinate_map):
    """
    Transform a coordinate map to a two-dimensional grid.

    :param coordinate_map: Map from Coordinate to Color.
    :return: A list of lists representing the same data as the map.
    """
    if not coordinate_map:
        return []

    max_row = max([coord.i for coord in coordinate_map.keys()])
    max_col = max([coord.j for coord in coordinate_map.keys()])

    return [
        [
            coordinate_map.get(Coordinate(i, j), EmptyColor())
            for j in range(max_col + 1)
        ]
        for i in range(max_row + 1)
    ]


def grid_to_coordinate_map(grid):
    """
    Transform a grid to a coordinate map.

    :param grid: A list of lists whose elements are Colors.
    :return: A map from Coordinate to Color.
    """
    return {
        Coordinate(i, j): grid[i][j]
        for i in range(len(grid))
        for j in range(len(grid[0]))
    }


def flatten(l):
    """
    Flatten a two-dimensional list.

    :param l: The two-dimensional list.
    :return: A one-dimensional, flattened list.
    """
    return [item for sublist in l for item in sublist]


class Board:
    """
    Representation of the game board.
    """

    def __init__(self, grid):
        """
        Construct a Board from a coordinate map.
        Do not call this method directly; rather, use the static from_coordinate_map and from_grid
        methods on Board. These static methods do proper input validation before directly calling
        this constructor.

        :param grid: The grid of colors representing the board.
        """
        self.board = grid
        self.coords = flatten((
            (
                Coordinate(i, j)
                for j in range(len(self.board[0]))
                if not self.board[i][j].is_empty()
            )
            for i in range(len(self.board))
        ))

    @staticmethod
    def from_coordinate_map(coordinate_map):
        """
        Create a board from a coordinate map.

        :param coordinate_map: A map from Coordinate to Color, which may be only partially complete.
        :return: A Board instance describing the input.
        """
        return Board.from_grid(coordinate_map_to_grid(coordinate_map))

    @staticmethod
    def from_grid(grid):
        """
        Create a board directly from a grid of Color.

        :param grid: A list of lists whose elements are Colors.
        :return: A Board instance describing the input.
        """
        return Board(grid)

    def is_solved(self):
        """
        Determine if the board is in a solved state.

        :return: True if the board is solved; False otherwise.
        """
        return not len(self.board)

    def flood_indices(self, coord):
        """
        For a given coordinate, get a list of valid indices that are in the same flood pool as the
        input coordinate.

        :param coord: Coordinate on this board.
        :return: A list of valid Coordinates in the input's flood pool.
        """
        queue = deque([coord])
        flood = set([])

        while len(queue) > 0:
            location = queue.popleft()
            flood.add(location)

            valid_neighbors = filter(
                lambda index: self.at(index) == self.at(coord) and index not in flood,
                self._get_neighbors(location),
            )
            queue.extend(valid_neighbors)

        return flood

    def available_moves(self):
        """
        Get a list of available moves and resulting board configurations.

        :return: A list of tuples, each of which is of the shape (Coordinate, Board). The first
                 element represents the coordinate from which a flood pool was popped, and the
                 second element represents the Board instance resulting from that action.
        """
        pools = set([])

        moves = []
        for coord in self.coords:
            try:
                new_board = self.pop_from(coord)
                if str(new_board) not in pools:
                    pools.add(str(new_board))
                    moves.append((coord, new_board))
            except InvalidPopException:
                pass

        return moves

    def pop_from(self, coord):
        """
        Determine the board configuration resulting from an attempted flood pool pop at the
        specified coordinate.

        :param coord: Coordinate on this board.
        :return: A new Board resulting from popping the flood pool at the given location.
        :raises InvalidPopException: If a pop is not allowed from the given coordinate.
        """
        # Get a list of all the indices that can be popped from this location
        to_pop = self.flood_indices(coord)

        # The game forbids popping an index where the flood size is unity
        if len(to_pop) == 1:
            raise InvalidPopException('Unable to pop from a flood group with only one element')

        # Create a new grid with popped items changed to EmptyColors
        update_grid = filter(lambda elem: elem, [
            [
                EmptyColor() if Coordinate(i, j) in to_pop else self.at(Coordinate(i, j))
                for j in range(len(self.board[i]))
            ]
            for i in range(len(self.board))
        ])

        return Board.from_grid(update_grid).contract()

    def contract(self):
        """
        Generate a new Board whose columns and rows are contracted.

        :return: A board instance whose physical configuration is contracted.
        """
        return self._contract_cols()._contract_rows()

    def at(self, coord):
        """
        Retrieve the Color at a particular coordinate location.

        :param coord: Coordinate on this board.
        :return: The Color at the specified location or None if the coordinate is invalid.
        """
        return self.board[coord.i][coord.j]

    def _is_coordinate_valid(self, coord):
        """
        Check if the specified coordinate is valid on this board.

        :param coord: Coordinate on this board.
        :return: True if the coordinate exists on this board; False otherwise.
        """
        return 0 <= coord.i < len(self.board) and 0 <= coord.j < len(self.board[0])

    def _get_neighbors(self, coord):
        """
        For a given coordinate, get a list of valid neighboring locations. Game rules dictate that
        the neighbor can only be immediately above, below, or to the side of the origin coordinate.

        :param coord: Coordinate on this board.
        :return: A list of valid Coordinate neighbors.
        """
        neighboring_coordinates = [
            Coordinate(coord.i + i_offset, coord.j + j_offset)
            for i_offset, j_offset in [(-1, 0), (0, 1), (1, 0), (0, -1)]
        ]

        return filter(self._is_coordinate_valid, neighboring_coordinates)

    def _contract_cols(self):
        """
        Contract columns of the board. This involves completely eliminating columns that contain
        only EmptyColors; e.g., all Colors that exist to the right of the empty column can be
        shifted to the left.

        :return: A new Board whose columns are contracted.
        """
        # Build a map of the number of empty rows in each column
        col_empty_counts = {
            col: len(filter(lambda elem: elem.is_empty(), self._extract_col(col)))
            for col in range(len(self.board[0]))
        }

        # Get a list of all the columns that need to be removed
        to_remove_cols = filter(
            lambda col: col_empty_counts[col] == len(self.board),
            col_empty_counts.keys(),
        )

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
        """
        Contract rows of the board. This involves dropping colors to be as close to the bottom of
        the board as possible. Generally, the Board returned by this procedure will be different
        from the existing board only if there exists at least one EmptyColor vertically separating
        two or more Colors.

        :return: A new Board whose rows are contracted.
        """
        # For each column, determine indices in that column that are empty
        col_empty_indices = {
            col: [idx for idx, elem in enumerate(self._extract_col(col)) if elem.is_empty()]
            for col in range(len(self.board[0]))
        }

        # Generate a list where each sublist is a properly contracted version of each column
        shifted_cols = [
            ([EmptyColor()] * len(col_empty_indices[idx])) + filter(
                lambda elem: not elem.is_empty(),
                self._extract_col(idx)
            )
            for idx in range(len(self.board[0]))
        ]

        # In order to create a grid again, the columns generated above need to be transposed
        return Board.from_grid(zip(*shifted_cols))

    def _extract_col(self, col):
        """
        Extract a single column index from the board as a single list.

        :param col: Column index to extract.
        :return: A list that is the single extracted column.
        """
        return [
            row[col]
            for row in self.board
        ]

    def __repr__(self):
        """
        Generate a string representation of the board. EmptyColors are marked with dashes equal in
        length as Colors.

        :return: A string representation of the board.
        """
        colors = set(filter(lambda loc: not loc.is_empty(), flatten(self.board)))
        color_length = max(map(len, colors) or [''])

        return '\n'.join([
            ' '.join(map(
                lambda elem: '-' * color_length if elem.is_empty() else str(elem),
                self.board[row],
            ))
            for row in range(len(self.board))
        ])


class InvalidPopException(Exception):
    """
    Raised when a pop is attempted at a location whose flood pool only consists of the single
    input element.
    """
    pass
