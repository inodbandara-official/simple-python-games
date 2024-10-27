import random
import PySimpleGUI as sg  # Make sure this is installed correctly with `pip install PySimpleGUI`

# Constants for the game
GRID_SIZE = 4
TARGET = 2048
EMPTY_TILE = 0

# Initialize the game board
def init_board():
    board = [[EMPTY_TILE] * GRID_SIZE for _ in range(GRID_SIZE)]
    add_new_tile(board)
    add_new_tile(board)
    return board

# Add a new tile (2 or 4) to the board
def add_new_tile(board):
    empty_tiles = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if board[r][c] == EMPTY_TILE]
    if empty_tiles:
        r, c = random.choice(empty_tiles)
        board[r][c] = 2 if random.random() < 0.9 else 4

# Merge the tiles in the specified direction
def merge_tiles(board, direction):
    if direction in ["UP", "DOWN"]:
        for col in range(GRID_SIZE):
            tiles = [board[row][col] for row in range(GRID_SIZE) if board[row][col] != EMPTY_TILE]
            new_tiles = merge_line(tiles)
            for row in range(GRID_SIZE):
                board[row][col] = new_tiles[row] if row < len(new_tiles) else EMPTY_TILE
    else:
        for row in range(GRID_SIZE):
            tiles = [board[row][col] for col in range(GRID_SIZE) if board[row][col] != EMPTY_TILE]
            new_tiles = merge_line(tiles)
            for col in range(GRID_SIZE):
                board[row][col] = new_tiles[col] if col < len(new_tiles) else EMPTY_TILE

# Merge a line of tiles
def merge_line(tiles):
    merged = []
    skip = False
    for i in range(len(tiles)):
        if skip:
            skip = False
            continue
        if i < len(tiles) - 1 and tiles[i] == tiles[i + 1]:
            merged.append(tiles[i] * 2)
            skip = True
        else:
            merged.append(tiles[i])
    return merged

# Check if the game is over
def is_game_over(board):
    if any(EMPTY_TILE in row for row in board):
        return False
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if (r < GRID_SIZE - 1 and board[r][c] == board[r + 1][c]) or (c < GRID_SIZE - 1 and board[r][c] == board[r][c + 1]):
                return False
    return True

# Create the GUI for the game
def create_window(board):
    layout = [
        [sg.Text('Score:', size=(10, 1), font=("Helvetica", 16), key='score')],
    ]
    for r in range(GRID_SIZE):
        row = []
        for c in range(GRID_SIZE):
            row.append(sg.Button('', size=(4, 2), font=('Helvetica', 24), key=(r, c), pad=(1, 1)))
        layout.append(row)
    return sg.Window('2048', layout, return_keyboard_events=True, finalize=True)

# Get the current score based on the board
def get_score(board):
    return sum(sum(row) for row in board)

# Main game loop
def main():
    board = init_board()
    window = create_window(board)

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Escape'):
            break

        # Determine the move based on the key pressed
        if event in ('Up:38', 'w'):
            merge_tiles(board, 'UP')
        elif event in ('Down:40', 's'):
            merge_tiles(board, 'DOWN')
        elif event in ('Left:37', 'a'):
            merge_tiles(board, 'LEFT')
        elif event in ('Right:39', 'd'):
            merge_tiles(board, 'RIGHT')

        add_new_tile(board)

        # Update the window
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                text = str(board[r][c]) if board[r][c] != EMPTY_TILE else ''
                window[(r, c)].update(text=text, button_color=('black', 'white' if board[r][c] != EMPTY_TILE else 'black'))

        window['score'].update(f'Score: {get_score(board)}')

        if is_game_over(board):
            sg.popup('Game Over!', title='2048')
            break

    window.close()

# Run the game
if __name__ == '__main__':
    main()
