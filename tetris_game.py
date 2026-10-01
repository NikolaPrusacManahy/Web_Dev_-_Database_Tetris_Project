import tetrisplay

grid = tetrisplay.build_clean_grid()

while True:
    col = tetrisplay.pick_random_column(grid)
    if col is None:                 # no column has room left
        break
    grid = tetrisplay.drop_and_land(grid, col)

print("GAME OVER")