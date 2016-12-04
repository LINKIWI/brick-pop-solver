class Color:
    def __init__(self, name):
        self.name = name

    def is_empty(self):
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


class EmptyColor(Color):
    def __init__(self):
        Color.__init__(self, 'EMPTY')

    def is_empty(self):
        return True
