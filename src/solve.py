import Queue
import multiprocessing
import struct
import subprocess
import sys
import time

import cv2
import numpy as np

from board import Board
from color import Color
from color import EmptyColor
from coordinate import Coordinate
from solution import EmptySolution
from solution import Solution

# The pixel offset distance between any two color blocks
IMAGE_BLOCK_OFFSET = 142
# The vertical pixel offset from the top of the screen of the first color block
IMAGE_BLOCK_START_I = 625
# The horizontal pixel offset from the left of the screen of the first color block
IMAGE_BLOCK_START_J = 70


def solution_search(queue, available_moves, steps=tuple([])):
    """
    Find a solution to the board given a list of available moves. This is a parallel-friendly
    implementation that executes a DFS search with defined starting points.

    :param queue: A queue into which a solution will be inserted when found.
    :param available_moves: A list of the shape [(Coordinate, Board), ...] representing a potential
                            solution step and the resulting board, respectively.
    :param steps: The steps taken thus far to reach the board configurations specified by
                  available_moves.
    :return: Return value is unused.
    """
    for step, board in available_moves:
        solution_steps = steps + (step,)
        if board.is_solved():
            return queue.put(Solution(solution_steps))

        solution_search(queue, board.available_moves(), solution_steps)

    if not steps:
        # If logic reaches this point in execution and there are no valid steps built up yet, the
        # input board configuration is not solvable. An EmptySolution is inserted into the queue,
        # and logic higher up the stack handles this appropriately.
        return queue.put(EmptySolution())


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
            pixel_i = IMAGE_BLOCK_START_I + i * IMAGE_BLOCK_OFFSET
            pixel_j = IMAGE_BLOCK_START_J + j * IMAGE_BLOCK_OFFSET
            bgr = img[pixel_i][pixel_j]
            color_code = struct.pack('BBB', *bgr).encode('hex')
            if color_code == 'e4eff7':
                coordinate_map[Coordinate(i, j)] = EmptyColor()
            else:
                coordinate_map[Coordinate(i, j)] = Color(color_code)

    return Board.from_coordinate_map(coordinate_map)


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

    for coord in board.coords:
        img_coord = Coordinate(
            IMAGE_BLOCK_START_I + IMAGE_BLOCK_OFFSET * coord.i,
            IMAGE_BLOCK_START_J + IMAGE_BLOCK_OFFSET * coord.j,
        )
        for i in range(img_coord.i - 50, img_coord.i + 50):
            for j in range(img_coord.j - 50, img_coord.j + 50):
                if coord == step:
                    img[i][j] = (255, 255, 255)
                else:
                    color_hex = board.at(coord).name.decode('hex')
                    img[i][j] = np.array(struct.unpack('BBB', color_hex))

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
        subprocess.call(['sleep', '1.2'])


def serial_solve(board, steps=tuple([])):
    """
    Solve the board using a serial DFS search. This is a single-threaded implementation that
    explores all possible solutions from a starting board configuration.

    :param board: The board to solve.
    :param steps: The steps taken thus far to reach the input board configuration.
    :return: A tuple of Coordinates representing steps that can be used to solve the board.
    """
    if board.is_solved():
        return Solution(steps)

    possible_solutions = (
        serial_solve(new_board, steps + (step,))
        for (step, new_board) in board.available_moves()
    )
    valid_solutions = (
        steps
        for steps in possible_solutions
        if not steps.is_empty()
    )

    return next(valid_solutions, EmptySolution())


def parallel_solve(board):
    """
    Solve the board in parallel by generating multiple starting points and attempting to find a
    solution for each of them using multiple, independent processes with access to a shared-memory
    data structure.

    :param board: An instance of the game board.
    :return: A valid solution as generated by one of the parallel processes.
    """
    # Start a shared-memory queue that all processes can mutate; any one process can insert a valid
    # solution in the queue
    queue = multiprocessing.Queue()

    # Divide the input into equal parts matching the number of parallel processes to use
    processes = [
        multiprocessing.Process(target=solution_search, args=(queue, [single_start_point],))
        for single_start_point in board.available_moves()
    ]

    # Start each individual process
    for p in processes:
        p.start()

    # The logic that follows involves trying to (asynchronously) retrieve an item from the
    # shared-memory queue. The queue can contain either a valid solution or an empty solution.
    solution = EmptySolution()
    num_failed_solves = 0
    while True:
        if num_failed_solves >= len(processes):
            # If we have failed the same number as times as there are processes, that means all
            # starting points were not able to return a valid solution. In this case, the only
            # recourse is to exit, and allow logic higher up the stack to handle an EmptySolution.
            break

        try:
            # Attempt to pull from the queue, without blocking. These operations are thread-safe.
            solution = queue.get(block=False)
            if solution.is_empty():
                # One processes has failed to create a solution; keep track of this in a (pseudo-
                # atomic) counter variable.
                num_failed_solves += 1
            else:
                # A valid solution has been found!
                break
        except Queue.Empty:
            # Since the Queue#get operation is non-blocking, most calls will throw an exception
            # indicating that there are no values to retrieve from the queue. In this case, simply
            # try again indefinitely.
            pass

    # Kill the remaining processes; we've already found a solution and they don't need to be around
    # anymore
    for p in processes:
        p.terminate()

    # Join the processes
    p.join()

    return solution


def solve(board_image_file_name):
    """
    Run the full solve procedure on some input board screenshot.

    :param board_image_file_name: Path to the screenshot of the board.
    """
    print 'Reading board image...'
    board = load_board(board_image_file_name)

    print 'Board:'
    print board

    print 'Solving...'
    start_time = time.time()
    solution = parallel_solve(board)
    end_time = time.time()

    if not solution.is_empty():
        print 'Found a solution in {duration} seconds'.format(duration=end_time - start_time)
    else:
        print 'The input board configuration has no solution!'
        sys.exit(1)

    solution_steps = solution.get_steps()
    print 'Solution ({num_steps} steps):'.format(num_steps=len(solution_steps))
    print solution_steps

    print 'Using ADB to trigger touch events...'
    simulate_touch_events(solution_steps)

    print 'Done!'


def main():
    """
    Main procedure; accept the file name as a command-line parameter and run the solver.
    """
    if len(sys.argv) < 2:
        print 'Specify the file name corresponding to the Brick Pop screenshot as the first ' \
              'positional argument.'
        sys.exit(1)

    solve(sys.argv[1])


if __name__ == '__main__':
    main()
