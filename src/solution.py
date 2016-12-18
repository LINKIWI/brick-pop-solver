class Solution:
    """
    Wrapper class representing a non-null, defined solution.
    """

    def __init__(self, steps):
        """
        Steps to the solution.

        :param steps: An iterable of Coordinates representing a solution.
        """
        self.steps = steps

    def is_empty(self):
        """
        A defined solution is defined to be non-empty.

        :return: False, always.
        """
        return False

    def get_steps(self):
        """
        Retrieve the steps associated with this solution.

        :return: The solution steps.
        """
        return self.steps

    def __eq__(self, other):
        return self.steps == other.steps

    def __repr__(self):
        return 'Solution({steps})'.format(steps=repr(self.steps))

    def __str__(self):
        return repr(self)


class EmptySolution(Solution):
    """
    Wrapper class representing a null solution.
    """

    def __init__(self):
        """
        Create an empty solution.
        """
        Solution.__init__(self, tuple([]))

    def is_empty(self):
        """
        An empty solution is defined to be empty.

        :return: True, always.
        """
        return True

    def get_steps(self):
        """
        Getting the solution steps for an empty solution is inherently undefined.

        :raises EmptySolutionException: Always.
        """
        raise EmptySolutionException('Attempt to retrieve a solution from an EmptySolution')

    def __repr__(self):
        return 'EmptySolution()'


class EmptySolutionException(Exception):
    """
    Exception raised when attempting to retrieve solution steps out of an empty solution.
    """
    pass
