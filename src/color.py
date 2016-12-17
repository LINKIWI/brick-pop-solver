class Color:
    """
    Representation of an element on the game board.
    """

    def __init__(self, name):
        """
        Create a new board item.

        :param name: Hexadecimal representation of the color, e.g. 'FFFFFF'.
        """
        self.name = name

    def is_empty(self):
        """
        A Color item on a board is not empty.

        :return: False, always.
        """
        return False

    def __eq__(self, other):
        return isinstance(other, Color) and self.name == other.name

    def __repr__(self):
        return str(self.name)

    def __str__(self):
        return repr(self)

    def __cmp__(self, other):
        return cmp(self.name, other)

    def __hash__(self):
        return hash(self.name)

    def __len__(self):
        return len(self.name)


class EmptyColor(Color):
    """
    Representation of an empty element on the game board (e.g. a space that has already been
    cleared).
    """

    def __init__(self):
        """
        Create an empty board item.
        """
        Color.__init__(self, 'EMPTY')

    def is_empty(self):
        """
        An EmptyColor is defined as empty.

        :return: True, always.
        """
        return True
