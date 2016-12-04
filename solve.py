from board import Board
from collections import deque
from color import Color
from coordinate import Coordinate
import cv2


class SolutionState:
    def __init__(self, board, steps):
        self.board = board
        self.steps = steps

    def __repr__(self):
        return '{board}\n{steps}'.format(board=str(self.board), steps=self.steps)


def solve_board(board):
    queue = deque([SolutionState(board, [])])

    while len(queue) > 0:
        print len(queue)
        state = queue.popleft()

        if state.board.is_solved():
            return state.steps

        for step, new_board in state.board.available_moves():
            queue.append(SolutionState(new_board, state.steps + [step]))

    return None


def replay_steps(board, steps):
    print steps[0]
    print board
    print ''

    if len(steps) == 1:
        return

    replay_steps(board.pop_from(steps[0]), steps[1:])


def load_board():
    img = cv2.imread('brick-pop.png', cv2.IMREAD_COLOR)

    start_i = 625
    offset_i = 140
    start_j = 70
    offset_j = 140

    coordinate_map = {}
    for i in range(10):
        for j in range(10):
            bgr = img[start_i + i * offset_i][start_j + j * offset_j]
            hex = '#%02x%02x%02x' % (bgr[2], bgr[1], bgr[0])
            coordinate_map[Coordinate(i, j)] = Color(hex)

    return Board(coordinate_map)


def solve():
    board = load_board()
    solution = solve_board(board)
    replay_steps(board, solution)


if __name__ == '__main__':
    solve()
