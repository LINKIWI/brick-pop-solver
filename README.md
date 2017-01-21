# brick-pop-solver

[![Build Status](https://travis-ci.org/LINKIWI/brick-pop-solver.svg?branch=master)](https://travis-ci.org/LINKIWI/brick-pop-solver) [![Coverage Status](https://coveralls.io/repos/github/LINKIWI/brick-pop-solver/badge.svg?branch=master)](https://coveralls.io/github/LINKIWI/brick-pop-solver?branch=master)

Automated solver for the [Brick Pop](https://techcrunch.com/2016/11/29/messenger-instant-games/) Facebook Messenger game.

[![Screencast](http://i.imgur.com/JNEHU0A.jpg)](https://www.youtube.com/watch?v=DVQx-ObS9I0)

At a high level, this program parses a screenshot of the board, generates a step-by-step solution by simulating brick-popping gameplay, and replays these events by using ADB to simulate touch events on an actual connected device to play through the solution for you.

### Related Projects

It's humbling to see the number of other open source [Brick Pop solvers](https://github.com/search?utf8=%E2%9C%93&q=brick+pop) inspired by this project. If this one doesn't work for you, please see the other solvers written in a variety of languages with several unique approaches (including one using a score-optimizing [beam search](https://en.wikipedia.org/wiki/Beam_search) algorithm).

### Algorithm Overview

The approach this program takes toward generating a solution is aggressive optimization of a search through a very large solution space. Effectively, the simulator considers every possible transition from one state/board configuration to another (based on some very simple rules, summarized below), and explores each of these paths using a depth-first search strategy.

In the worst case, there are six unique colors on a fixed-size 10x10 board, resulting in the possibility that each node uncovers anywhere between 10-20 additional potential solution paths. A breadth-first search would be computationally infeasible; the structure of the game is such that it is inherently more efficient to fully explore an entire route and check its validity rather than exhaust individual paths as they are uncovered from state transitions. This is because of the fact that any single input board configuration is likely to have several valid solution paths.

Fortunately, the gameplay rules are simple enough that the state transitions can be modeled very precisely:

1. Popping a brick from any location *(i, j)* recursively pops all bricks within its *flood pool*, defined as neighbors (and their neighbors thereof) who share the same color as the brick at *(i, j)*. The game defines a neighbor to be a block at *(i + 1, j)*, *(i - 1, j)*, *(i, j + 1)*, or *(i, j - 1)*. A pop is considered valid only if the size of the flood pool is greater than unity.
2. Popping a flood pool removes each brick in the flood pool from the board. This removal creates gaps in the board, which are resolved through a *contraction* process whereby columns are removed if every element in the column is empty, and non-null brick elements above (i.e. a colored brick at *(i, j)* and an empty brick at *(i + n, j)* for *n > 0*) are pushed as far as possible to the bottom of the board such that no empty blocks exist below it.
3. This process continues until there are zero non-null elements left on the board. Thus, the board is considered to be in a solved state if all bricks have been removed from the board via a flood pool pop.

This program makes use of no heuristics to generate a solution; rather, it only attempts to be clever in the way the solution space is searched.

### Performance and Parallelism

Since the entire solution space is searched until DFS finds a valid solution path, this program exploits multicore processing by dedicating a process to each available starting point on the board. This allows for multiple solution paths to be explored in parallel; once one process finds a valid solution, it returns this value and kills all other processes. This approach is inherently non-deterministic, but in practice, this process-based parallelism has decreased the amount of time taken to arrive at a solution by several orders of magnitude.

The implementation as-is defaults to a parallel solve, but this can be changed by substituting `parallel_solve` for `serial_solve` in `solve.py`.

Most boards can be solved in less than 10 seconds. On occasion, a solution might not be found until several hundred seconds in. Generally, if no solution is found after this amount of time, it helps to partially solve the board (i.e. eliminating one color) and running the solver again.

### Prerequisites

* ADB
* OpenCV Python library

### Usage

1. Connect your Android device. Enable USB debugging, and make sure it appears under `adb devices`
2. Open an instance of Brick Pop through Facebook Messenger. Start the game and start the first level (so that the blocks are visible).
3. Run `./brick-pop-solve.sh`. This will:
  1. Pull a screenshot from the connected device
  2. Parse out a board configuration from the screenshot
  3. Run the solver on the input board configuration and generate solution steps
  4. Use ADB to simulate touch events on the device to play through the generated solution

### Notes

* I've only tested this on my LG G4, which has a screen resolution of 1440x2560. Board generation from the screenshot is based on constant pixel offsets, so it will not work on any other resolutions without modifying the `IMAGE_BLOCK_OFFSET` and `IMAGE_BLOCK_START_x` constants in `solve.py`.
* The solver does not attempt to optimize for score or solution path length; it only guarantees a *valid* solution.

### Development

Initialize a virtualenv:

```bash
$ virtualenv env
$ source env/bin/activate
```

Install all dependencies:

```bash
$ make bootstrap
```

Run the linter:

```bash
$ make lint
```

Run all unit and integration tests:

```bash
$ make test
```

PRs must pass the [Travis](https://travis-ci.org/LINKIWI/brick-pop-solver) build to be accepted.
