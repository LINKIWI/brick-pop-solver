import os
import time


def time_func(target, *args, **kwargs):
    """
    Time the execution of a function.

    :param target: The target function.
    :param args: Arguments to the function.
    :param kwargs: Keyword arguments to the function.
    :return: The original return value of args and kwargs applied to the target.
    """
    start_time = time.time()
    ret = target(*args, **kwargs)
    end_time = time.time()
    return ret, end_time - start_time


def is_solution_valid(board, solution):
    """
    Check if a generated solution is valid for a given board.

    :param board: The original, starting board.
    :param solution: A full solution, i.e. a list of Coordinates.
    :return: True if the solution is valid; False otherwise.
    """
    if not solution:
        return board.is_solved()

    return is_solution_valid(board.pop_from(solution[0]), solution[1:])


def fixture_path(file_name):
    """
    Generate a path to the test fixture given the name of the file.

    :param file_name: The name of the test fixture file.
    :return: An absolute path to the test fixture.
    """
    cwd = os.path.dirname(__file__)
    return os.path.join(cwd, '../fixtures/{file_name}'.format(file_name=file_name))
