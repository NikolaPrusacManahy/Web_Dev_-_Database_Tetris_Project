import tetrisplay

grid = tetrisplay.build_clean_grid()
tetrisplay.start_keyboard()

col = tetrisplay.pick_random_column(grid)

# Keep dropping blocks for as long as there is a column with room.
# pick_random_column() returns None once every column is full.
while col != None:
    grid = tetrisplay.drop_and_land(grid, col)
    col = tetrisplay.pick_random_column(grid)

# No room left in the game
# happy days
print("GAME OVER")