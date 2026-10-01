_ROWS = 10
_COLUMNS = 5
_INTERVAL = 0.3
_BLANK = "  "
_BLOCK = "\u2588\u2588"


import time
import random
from IPython.display import clear_output

from pynput import keyboard


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
    # Blocks pile up from the bottom, so the TOP cell (row 0) is always the
    # last one to fill. If it is still blank, the column has room.
    return grid[column_number][0] == _BLANK


def pick_random_column(grid):
    """Return a random column that still has room, or None if all are full."""
    free_columns = [c for c in range(_COLUMNS) if column_has_room(grid, c)]
    # No free columns left means the board is full
    if len(free_columns) == 0:
        return None
    # Pick one of the free columns at random    
    return random.choice(free_columns)

# Remembers the last arrow key pressed: "left", "right" or None.
_last_key = None


def on_press(key):
    """Called automatically by pynput every time a key is pressed."""
    # global lets this function change the _last_key variable that is already defined above there,
    # instead of creating a new local variable with the same name.
    global _last_key
    if key == keyboard.Key.left:
        _last_key = "left"
    elif key == keyboard.Key.right:
        _last_key = "right"


def start_keyboard():
    """Start listening to the keyboard in the background."""
    # every time a key is pressed it
    # calls on_press(key) for me. We pass the function itself.
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    return listener


# Written with AI assistance: the function "move_sideways" was made with the help of Claude
def move_sideways(grid, column_number, row):
    """If an arrow was pressed, move the falling block one column left or right,
    only if that cell is inside the board and empty. Return the block's column."""
    global _last_key
    # Work out which column the player wants the block to move to.
    new_column = column_number
    if _last_key == "left":
        new_column = column_number - 1
    elif _last_key == "right":
        new_column = column_number + 1

    # The key press has now been dealt with, so forget it
    # (one press = one move).
    _last_key = None                     

    # Check the move is legal. If not, the block stays where it is.
    if new_column < 0:                    # off the left edge
        return column_number
    if new_column >= _COLUMNS:            # off the right edge
        return column_number
    if grid[new_column][row] == _BLOCK:   # a block is in the way
        return column_number

    # The move is legal: erase the block from the old column,
    # draw it in the new column, and redraw the board.
    grid[column_number][row] = _BLANK     # erase from old column
    grid[new_column][row] = _BLOCK        # draw in new column
    clear_output(wait=True)
    display_grid(grid)
    return new_column


def drop_and_land(grid, column_number):
    """Animate a block falling down a column. Arrow keys move it sideways.
    Stop when it reaches the bottom or lands on another block and leave it there."""
    global _last_key
    _last_key = None                      # ignore keys pressed before this block appeared
    row = 0
    landed = False

    while not landed:
        # Draw the block at its current position and show the board.
        grid[column_number][row] = _BLOCK
        clear_output(wait=True)
        display_grid(grid)

        # Instead of one long sleep, take 5 short ones and check the keys in between
        for i in range(5):
            time.sleep(_INTERVAL / 5)
            column_number = move_sideways(grid, column_number, row)
            
        # Checking if the block has landed
        if row == _ROWS - 1:                          # reached the bottom row
            landed = True
        elif grid[column_number][row + 1] == _BLOCK:  # a block is directly underneath
            landed = True
        else:                                         # still falling: erase and move down
            grid[column_number][row] = _BLANK
            row = row + 1

    return grid 