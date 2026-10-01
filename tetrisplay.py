_ROWS = 10
_COLUMNS = 5
_INTERVAL = 0.3
_BLANK = "  "
_BLOCK = "\u2588\u2588"


import time
import random
from IPython.display import clear_output


def build_clean_grid():
    """Reset the tetris grid to empty."""
    return [["  " for i in range(_ROWS)] for i in range(_COLUMNS)]


def drop_block(grid, column_number):
    """Given a column number, update the tetris grid to add a block to that column.
    Return the updated grid to the caller."""
    try:
        n = grid[column_number].index(_BLOCK)
        n = n - 1
    except:
        n = -1
    grid[column_number][n] = _BLOCK
    return grid


def display_grid(grid):
    """Display the current state of the tetris grid "vertically" up the screen. Remember: by default,
    the grid dispays across the screen, row-wise (which, usually, isn't what we want here)."""
    the_columns = tuple(range(0, _COLUMNS))
    the_rows = tuple(range(0, _ROWS))
    for r in the_rows:
        print("|", sep="", end="")
        for c in the_columns:
            print(grid[c][r], "|", sep="", end="")
        print()


def show_dropping_block(grid, column_number):
    """Given a grid and a column to drop into, simulate a visual drop of a box."""

    for row in range(_ROWS):
        grid[column_number][row] = _BLOCK
        display_grid(grid)
        time.sleep(_INTERVAL)
        clear_output(wait=True)
        grid[column_number][row] = _BLANK
        display_grid(grid)
        time.sleep(_INTERVAL)
        clear_output(wait=True)

def column_has_room(grid, column_number):
    """Return True if the top cell of this column is still blank."""
    return grid[column_number][0] == _BLANK


def pick_random_column(grid):
    """Return a random column that still has room, or None if all are full."""
    free_columns = [c for c in range(_COLUMNS) if column_has_room(grid, c)]
    if len(free_columns) == 0:
        return None
    return random.choice(free_columns)


def drop_and_land(grid, column_number):
    """Animate a block falling down a column. Stop when it reaches the
    bottom or lands on another block, and leave it there."""
    row = 0
    while True:
        grid[column_number][row] = _BLOCK      # draw block at current row
        clear_output(wait=True)
        display_grid(grid)
        time.sleep(_INTERVAL)

        # checking if it has landed. Either it's on the bottom row,
        # or the cell underneath is already filled.
        if row == _ROWS - 1 or grid[column_number][row + 1] == _BLOCK:
            break                              # stop, and leave it on the board

        grid[column_number][row] = _BLANK      # erase it, then move down one
        row = row + 1

    return grid    