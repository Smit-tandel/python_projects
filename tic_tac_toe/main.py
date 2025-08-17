import numpy as np
import random

# Initialize the board
board = np.full((3,3), "__")

# Check if the game is won
def game_won(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "__":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != "__":
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != "__":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "__":
        return board[0][2]
    return None

# Player input
def player_turn():
    while True:
        pos = input("Enter your move (row_col, e.g., 1_1): ")
        if "_" not in pos:
            print("Invalid format! Use row_col, e.g., 1_1")
            continue
        a, b = pos.split("_")
        if not(a.isdigit() and b.isdigit()):
            print("Invalid input! Enter numbers 0-2")
            continue
        a, b = int(a), int(b)
        if 0 <= a <= 2 and 0 <= b <= 2:
            if board[a][b] == "__":
                return a, b
            else:
                print("Position already occupied!")
        else:
            print("Invalid position! Enter numbers between 0 and 2")

# Almost perfect AI move
def ai_turn():
    empty_positions = [(i, j) for i in range(3) for j in range(3) if board[i][j] == "__"]
    
    # 1️⃣ Win if possible
    for i, j in empty_positions:
        board[i][j] = "O"
        if game_won(board) == "O":
            return i, j
        board[i][j] = "__"
    
    # 2️⃣ Block player if they can win
    for i, j in empty_positions:
        board[i][j] = "X"
        if game_won(board) == "X":
            board[i][j] = "__"
            return i, j
        board[i][j] = "__"
    
    # 3️⃣ Take center if free
    if board[1][1] == "__":
        return (1, 1)
    
    # 4️⃣ Take a corner if available
    corners = [(0,0), (0,2), (2,0), (2,2)]
    available_corners = [pos for pos in corners if board[pos] == "__"]
    if available_corners:
        return random.choice(available_corners)
    
    # 5️⃣ Take any side
    sides = [(0,1), (1,0), (1,2), (2,1)]
    available_sides = [pos for pos in sides if board[pos] == "__"]
    if available_sides:
        return random.choice(available_sides)
    
    return None  # No moves left

# Main game loop
def play_game():
    turn = "X"  # Player starts
    moves = 0
    while True:
        print("\nCurrent board:")
        print(board)
        
        if turn == "X":
            a, b = player_turn()
            board[a][b] = "X"
        else:
            move = ai_turn()
            if move is None:
                print("It's a draw!")
                break
            a, b = move
            board[a][b] = "O"
            print(f"AI placed O at {a}_{b}")
        
        moves += 1
        winner = game_won(board)
        if winner:
            print("\nFinal board:")
            print(board)
            if winner == "X":
                print("Congratulations! You won!")
            else:
                print("AI wins!")
            break
        
        if moves == 9:
            print("\nFinal board:")
            print(board)
            print("It's a draw!")
            break
        
        # Switch turn
        turn = "O" if turn == "X" else "X"

# Start the game
play_game()
