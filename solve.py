import cv2

from board import Board
from color import Color
from coordinate import Coordinate


class SolutionState:
    def __init__(self, board, steps):
        self.board = board
        self.steps = steps

    def __repr__(self):
        return '{board}\n{steps}'.format(board=str(self.board), steps=self.steps)


def solve_board_dfs(board, steps=[]):
    if board.is_solved():
        return steps

    for step, new_board in board.available_moves():
        solution = solve_board_dfs(new_board, steps + [step])
        if solution:
            return solution

    return None


def replay_steps(board, steps):
    if len(steps) <= 1:
        return

    new_board = board.pop_from(steps[0])
    print steps[0]
    print new_board
    print ''

    replay_steps(new_board, steps[1:])


def load_board():
    img = cv2.imread('brick-pop.png', cv2.IMREAD_COLOR)

    offset = 142
    start_i = 625
    start_j = 70

    coordinate_map = {}
    for i in range(10):
        for j in range(10):
            bgr = img[start_i + i * offset][start_j + j * offset]
            hex = '#%02x%02x%02x' % (bgr[2], bgr[1], bgr[0])
            coordinate_map[Coordinate(i, j)] = Color(hex)

    return Board(coordinate_map)


def solve():
    board = load_board()

    print board
    solution = solve_board_dfs(board)
    replay_steps(board, solution)
    print solution


if __name__ == '__main__':
    solve()
