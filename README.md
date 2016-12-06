# brick-pop-solver

Solver for the Brick Pop Facebook Messenger game.

At a high level, this program parses a screenshot of the board, generates a step-by-step solution by simulating brick-popping gameplay, and either (1) replays these events by generating screenshots detailing a solution or (2) uses ADB to simulate touch events on an actual connected device to play through the solution for you.

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
* It's actually unclear whether the game always generates solvable board configurations.
