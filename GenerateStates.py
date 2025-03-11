from itertools import combinations

def is_valid_board_flat(board_flat):
    # Convert the flat board into a 4x4 grid for validation
    board = [board_flat[i:i+4] for i in range(0, 16, 4)]

    # Check rows
    for row in board:
        if row[0] != 0 and row[0] == row[1] == row[2] == row[3]:
            return False

    # Check columns
    for col in range(4):
        if board[0][col] != 0 and board[0][col] == board[1][col] == board[2][col] == board[3][col]:
            return False

    # Check diagonals
    if board[0][0] != 0 and board[0][0] == board[1][1] == board[2][2] == board[3][3]:
        return False
    if board[0][3] != 0 and board[0][3] == board[1][2] == board[2][1] == board[3][0]:
        return False

    return True

def generate_balanced_boards_optimized():
    valid_Board_Dictionary={}
    
    cells = 16  # Total cells in a 4x4 board

    # Iterate over even numbers of moves (2, 4, ..., 16)
    for moves in range(2, cells + 1, 2):
        valid_boards = []
        half_moves = moves // 2

        # Get all combinations of positions for `1`s
        for ones_positions in combinations(range(cells), half_moves):
            # Remaining positions after placing `1`s
            remaining_positions = set(range(cells)) - set(ones_positions)

            # Get all combinations of positions for `2`s
            for twos_positions in combinations(remaining_positions, half_moves):
                # Create the flat board
                board_flat = [0] * cells
                for pos in ones_positions:
                    board_flat[pos] = 1
                for pos in twos_positions:
                    board_flat[pos] = 2

                # Validate the board
                if is_valid_board_flat(board_flat):
                    valid_boards.append(board_flat)
        
        valid_Board_Dictionary[cells-moves]=valid_boards

    return valid_Board_Dictionary

# Generate all valid balanced boards
balanced_boards = generate_balanced_boards_optimized()

import pickle 

with open(r'C:\Users\Rajdeep Das\Desktop\RL_Project\QuartoBot\OrbitoAllStates.pkl', 'wb') as file: 
	pickle.dump(balanced_boards, file) 

#%%
from itertools import combinations

def is_valid_board_flat(board_flat):
    # Convert the flat board into a 4x4 grid for validation
    board = [board_flat[i:i+4] for i in range(0, 16, 4)]

    # Check rows
    for row in board:
        if row[0] != 0 and row[0] == row[1] == row[2] == row[3]:
            return False

    # Check columns
    for col in range(4):
        if board[0][col] != 0 and board[0][col] == board[1][col] == board[2][col] == board[3][col]:
            return False

    # Check diagonals
    if board[0][0] != 0 and board[0][0] == board[1][1] == board[2][2] == board[3][3]:
        return False
    if board[0][3] != 0 and board[0][3] == board[1][2] == board[2][1] == board[3][0]:
        return False

    return True

def generate_boards_player2_turn():
    valid_boards = []
    cells = 16  # Total cells in a 4x4 board

    # Iterate over odd numbers of moves (3, 5, ..., 15)
    for moves in range(3, cells + 1, 2):
        player1_moves = (moves + 1) // 2  # Player 1's moves (more by 1)
        player2_moves = moves // 2        # Player 2's moves

        # Get all combinations of positions for `1`s (Player 1)
        for ones_positions in combinations(range(cells), player1_moves):
            # Remaining positions after placing `1`s
            remaining_positions = set(range(cells)) - set(ones_positions)

            # Get all combinations of positions for `2`s (Player 2)
            for twos_positions in combinations(remaining_positions, player2_moves):
                # Create the flat board
                board_flat = [0] * cells
                for pos in ones_positions:
                    board_flat[pos] = 1
                for pos in twos_positions:
                    board_flat[pos] = 2

                # Validate the board
                if is_valid_board_flat(board_flat):
                    valid_boards.append(board_flat)

    return valid_boards

# Generate all valid boards where Player 2 is about to move
boards_player2_turn = generate_boards_player2_turn()

# Print the count and a few examples
print(f"Total valid boards where Player 2 is about to move: {len(boards_player2_turn)}")
print("Example valid board:")
for row in [boards_player2_turn[0][i:i+4] for i in range(0, 16, 4)]:
    print(row)

