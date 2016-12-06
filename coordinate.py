class Coordinate:
    """
    Representation of an (i, j)-indexed two-dimensional coordinate.
    """

    def __init__(self, i, j):
        """
        Create a new Coordinate.

        :param i: The vertical index.
        :param j: The horizontal index.
        """
        self.i = i
        self.j = j

    def offset(self, i_offset, j_offset):
        """
        Offset this coordinate by a constant horizontal and vertical amount.

        :param i_offset: The vertical offset to apply.
        :param j_offset:  The horizontal offset to apply.
        :return: A new Coordinate with the specified offsets applied.
        """
        return Coordinate(self.i + i_offset, self.j + j_offset)

    def __eq__(self, other):
        return isinstance(other, Coordinate) and self.i == other.i and self.j == other.j

    def __repr__(self):
        return '({i}, {j})'.format(i=self.i, j=self.j)

    def __str__(self):
        return repr(self)

    def __cmp__(self, other):
        if self.i < other.i or (self.i == other.i and self.j < other.j):
            return -1
        if self.j > other.j:
            return 1
        return 0

    def __hash__(self):
        return (self.i * 0x1f1f1f1f) ^ self.j
