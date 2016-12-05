class Coordinate:
    """
    Representation of an (i, j)-indexed two-dimensional coordinate.
    """

    def __init__(self, i, j):
        self.i = i
        self.j = j

    def tuple(self):
        return self.i, self.j

    def offset(self, i_offset, j_offset):
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
