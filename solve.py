import cv2
import numpy as np
import struct

from board import Board
from color import Color
from color import EmptyColor
from coordinate import Coordinate


class SolutionState:
    def __init__(self, board, steps):
        self.board = board
        self.steps = steps

    def __repr__(self):
        return '{board}\n{steps}'.format(board=str(self.board), steps=self.steps)


def solve_board_dfs(board, steps=tuple([])):
    if board.is_solved():
        return steps

    possible_solutions = (
        solve_board_dfs(new_board, steps + (step,))
        for (step, new_board) in board.available_moves()
    )
    valid_solutions = (
        steps
        for steps in possible_solutions
        if steps is not None
    )

    return next(valid_solutions, None)


def replay_steps(board, steps, idx=0):
    if len(steps) <= 1:
        return

    display_step(board, steps[0], 'step-{idx}.png'.format(idx=idx))
    replay_steps(board.pop_from(steps[0]), steps[1:], idx=idx + 1)


def load_board():
    img = cv2.imread('brick-pop.png', cv2.IMREAD_COLOR)

    offset = 142
    start_i = 625
    start_j = 70

    coordinate_map = {}
    for i in range(10):
        for j in range(10):
            bgr = img[start_i + i * offset][start_j + j * offset]
            hex = struct.pack('BBB', *bgr).encode('hex')
            if hex == 'e4eff7':
                coordinate_map[Coordinate(i, j)] = EmptyColor()
            else:
                coordinate_map[Coordinate(i, j)] = Color(hex)

    return Board(coordinate_map)


def display_step(board, step, file_name):
    img = np.array([
        [(0, 0, 0) for _ in range(1440)]
        for _ in range(2560)
    ])

    for coord in board.coordinate_map:
        img_coord = Coordinate(625 + 142 * coord.i, 70 + 142 * coord.j)
        for i in range(img_coord.i - 50, img_coord.i + 50):
            for j in range(img_coord.j - 50, img_coord.j + 50):
                if coord == step:
                    img[i][j] = (255, 255, 255)
                else:
                    img[i][j] = np.array(struct.unpack('BBB', board.at(coord).name.decode('hex')))

    cv2.imwrite(file_name, img)


def write_adb_script(solution):
    fd = open('script.sh', 'w')

    for idx, step in enumerate(solution):
        x = 70 + 142 * step.j
        y = 625 + 142 * step.i

        fd.write('echo Simulating touch events for step {idx}...\n'.format(idx=idx))
        fd.write('adb shell input tap {x} {y}\n'.format(x=x, y=y))
        fd.write('sleep 1\n')

    fd.close()


def solve():
    print 'Reading board image...'
    board = load_board()

    print 'Board:'
    print board
    print 'Colors:'
    print board.colors()

    print 'Solving...'
    solution = solve_board_dfs(board)
    write_adb_script(solution)
    print solution


if __name__ == '__main__':
    solve()
