import PySimpleGUI as sg
import random

# Constants
GRID_SIZE = 5
MINES = 3

# Create the Minesweeper grid
def create_grid(size, mines):
    grid = [[' ' for _ in range(size)] for _ in range(size)]
    mine_positions = random.sample(range(size * size), mines)
    for pos in mine_positions:
        row, col = divmod(pos, size)
        grid[row][col] = '*'
    return grid

# Count adjacent mines for each cell
def count_adjacent_mines(grid):
    size = len(grid)
    for row in range(size):
        for col in range(size):
            if grid[row][col] == '*':
                continue
            count = sum(1 for r in range(row-1, row+2) 
                         for c in range(col-1, col+2) 
                         if 0 <= r < size and 0 <= c < size and grid[r][c] == '*')
            grid[row][col] = str(count) if count > 0 else ' '
    return grid

# Main game function
def minesweeper_game():
    sg.theme('LightBlue')
    
    # Initialize the game
    grid = create_grid(GRID_SIZE, MINES)
    grid = count_adjacent_mines(grid)
    revealed = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    
    layout = [[sg.Button(revealed[row][col], key=(row, col), size=(4, 2)) for col in range(GRID_SIZE)] for row in range(GRID_SIZE)]
    layout.append([sg.Button("Reset"), sg.Button("Exit")])
    
    window = sg.Window("Minesweeper", layout)

    while True:
        event, _ = window.read()

        if event == sg.WINDOW_CLOSED or event == "Exit":
            break
        if event == "Reset":
            grid = create_grid(GRID_SIZE, MINES)
            grid = count_adjacent_mines(grid)
            revealed = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
            for row in range(GRID_SIZE):
                for col in range(GRID_SIZE):
                    window[(row, col)].update(' ')
            continue
        
        if isinstance(event, tuple):
            row, col = event
            if grid[row][col] == '*':
                sg.popup("Game Over! You hit a mine.")
                for r in range(GRID_SIZE):
                    for c in range(GRID_SIZE):
                        revealed[r][c] = grid[r][c]
                        window[(r, c)].update(revealed[r][c])
            else:
                revealed[row][col] = grid[row][col]
                window[(row, col)].update(revealed[row][col])

    window.close()

if __name__ == "__main__":
    minesweeper_game()
