# BattleDot Game

BattleDot is a multi-threaded simulation game where players compete by "bombing" each other's positions on a grid. Each player is represented by a thread, and the game continues until only one player remains.

## Requirements

- Python 3.6 or higher

## Setup

Please clone this repository into a directory of your choice. No compilation is necessary as the game is written in Python. However, you need to ensure Python 3 is installed on your system.

## Running the Game

To run the game, you can use the command line interface. Navigate to the directory containing the game script (`battledot.py`) and run:

```bash
python3 battledot.py
```

## Interpreting the Results

The game outputs each player's action to the console, including who is bombing whom and at which grid position. When a player's ship is hit, a message indicating that the player is out is displayed.

**Example Output**

- A bombing B at (3, 5)

- B bombing C at (2, 4)

- C bombing A at (3, 5)

- A has been hit and is out!

- B bombing C at (1, 1)

- C bombing B at (0, 0)

- B has been hit and is out!

Game over. C is the winner!

**This output indicates the following:**

- Player A bombs Player B at position (3, 5).

- Player B bombs Player C at position (2, 4).

- Player C bombs Player A at position (3, 5), resulting in Player A being hit and eliminated.

- The game continues until only one player remains. In our case, C.
