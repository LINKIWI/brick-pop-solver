import struct
import subprocess
import sys

import cv2
import numpy as np

from board import Board
from color import Color
from color import EmptyColor
from coordinate import Coordinate

# The pixel offset distance between any two color blocks
IMAGE_BLOCK_OFFSET = 142
# The vertical pixel offset from the top of the screen of the first color block
IMAGE_BLOCK_START_I = 625
# The horizontal pixel offset from the left of the screen of the first color block
IMAGE_BLOCK_START_J = 70


def solve_board_dfs(board, steps=tuple([])):
    """
    Solve the board using a DFS search.

    :param board: The board to solve.
    :param steps: The number of steps taken thus far to reach the input board configuration.
    :return: A tuple of Coordinates representing steps that can be used to solve the board.
    """
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
    """
    Given the initial board and a series of steps, generate image renders representing the block
    locations to be popped for each step.

    :param board: The initial board configuration.
    :param steps: A tuple of steps to take on the initial board.
    :param idx: The initial step index.
    """
    if not len(steps):
        return

    render_step_image(board, steps[0], 'step-{idx}.png'.format(idx=idx))
    replay_steps(board.pop_from(steps[0]), steps[1:], idx=idx + 1)


def load_board(board_image_file_name):
    """
    Parse the input board screenshot into a Board object.

    :param board_image_file_name: Path to the screenshot of the board.
    :return: A Board instance representing the input board.
    """
    img = cv2.imread(board_image_file_name, cv2.IMREAD_COLOR)

    coordinate_map = {}
    for i in range(10):
        for j in range(10):
            bgr = img[IMAGE_BLOCK_START_I + i * IMAGE_BLOCK_OFFSET][IMAGE_BLOCK_START_J + j * IMAGE_BLOCK_OFFSET]
            color_code = struct.pack('BBB', *bgr).encode('hex')
            if color_code == 'e4eff7':
                coordinate_map[Coordinate(i, j)] = EmptyColor()
            else:
                coordinate_map[Coordinate(i, j)] = Color(color_code)

    return Board(coordinate_map)


def render_step_image(board, step, file_name):
    """
    Render an image representing the step to take on a board. The desired step coordinate is
    highlighted in white.

    :param board: The current board configuration.
    :param step: The desired step to visualize.
    :param file_name: The file name to which the rendered image should be saved.
    """
    img = np.array([
        [(0, 0, 0) for _ in range(1440)]
        for _ in range(2560)
    ])

    for coord in board.coordinate_map:
        img_coord = Coordinate(
            IMAGE_BLOCK_START_I + IMAGE_BLOCK_OFFSET * coord.i,
            IMAGE_BLOCK_START_J + IMAGE_BLOCK_OFFSET * coord.j,
        )
        for i in range(img_coord.i - 50, img_coord.i + 50):
            for j in range(img_coord.j - 50, img_coord.j + 50):
                if coord == step:
                    img[i][j] = (255, 255, 255)
                else:
                    img[i][j] = np.array(struct.unpack('BBB', board.at(coord).name.decode('hex')))

    cv2.imwrite(file_name, img)


def simulate_touch_events(solution):
    """
    Directly use ADB to simulate touch events that correspond to the given solution steps.

    :param solution: A tuple of coordinates describing the full solution.
    """
    for idx, step in enumerate(solution):
        touch_x = IMAGE_BLOCK_START_J + IMAGE_BLOCK_OFFSET * step.j
        touch_y = IMAGE_BLOCK_START_I + IMAGE_BLOCK_OFFSET * step.i

        print 'Simulating touch events for step {idx}...'.format(idx=idx + 1)
        subprocess.call(['adb', 'shell', 'input', 'tap', str(touch_x), str(touch_y)])
        subprocess.call(['sleep', '1'])


def solve(board_image_file_name):
    """
    Run the full solve procedure on some input board screenshot.

    :param board_image_file_name: Path to the screenshot of the board.
    """
    print 'Reading board image...'
    board = load_board(board_image_file_name)

    print 'Board:'
    print board
    print 'Colors:'
    print board.colors()

    print 'Solving...'
    solution = solve_board_dfs(board)

    print 'Solution ({num_steps} steps):'.format(num_steps=len(solution))
    print solution

    print 'Using ADB to trigger touch events...'
    simulate_touch_events(solution)


def main():
    """
    Main procedure; accept the file name as a command-line parameter and run the solver.
    """
    if len(sys.argv) < 2:
        print 'Specify the file name corresponding to the Brick Pop screenshot as the first positional argument.'
        sys.exit(1)

    solve(sys.argv[1])


if __name__ == '__main__':
    main()
