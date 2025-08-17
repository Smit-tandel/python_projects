import tkinter as tk
import random

# Initialize the board
board = [["__" for _ in range(3)] for _ in range(3)]

# Check if game is won
def game_won():
    # Rows and columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "__":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != "__":
            return board[0][i]
    # Diagonals
    if board[0][0] == board[1][1] == board[2][2] != "__":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "__":
        return board[0][2]
    return None

# AI move
def ai_turn():
    empty_positions = [(i, j) for i in range(3) for j in range(3) if board[i][j] == "__"]
    
    # Win if possible
    for i, j in empty_positions:
        board[i][j] = "O"
        if game_won() == "O":
            return i, j
        board[i][j] = "__"
    
    # Block player
    for i, j in empty_positions:
        board[i][j] = "X"
        if game_won() == "X":
            board[i][j] = "__"
            return i, j
        board[i][j] = "__"
    
    # Center
    if board[1][1] == "__":
        return (1,1)
    
    # Corners
    corners = [(0,0),(0,2),(2,0),(2,2)]
    available_corners = [pos for pos in corners if board[pos[0]][pos[1]] == "__"]
    if available_corners:
        return random.choice(available_corners)
    
    # Sides
    sides = [(0,1),(1,0),(1,2),(2,1)]
    available_sides = [pos for pos in sides if board[pos[0]][pos[1]] == "__"]
    if available_sides:
        return random.choice(available_sides)
    
    return None

# Button click handler
def click(i,j):
    if board[i][j] == "__" and not game_won():
        board[i][j] = "X"
        buttons[i][j]["text"] = "X"
        
        winner = game_won()
        if winner:
            result_label["text"] = f"{winner} wins!"
            return
        # AI move
        move = ai_turn()
        if move:
            a,b = move
            board[a][b] = "O"
            buttons[a][b]["text"] = "O"
        
        winner = game_won()
        if winner:
            result_label["text"] = f"{winner} wins!"
        elif all(board[r][c] != "__" for r in range(3) for c in range(3)):
            result_label["text"] = "Draw!"

# Reset game
def reset():
    for i in range(3):
        for j in range(3):
            board[i][j] = "__"
            buttons[i][j]["text"] = ""
    result_label["text"] = ""

# GUI setup
root = tk.Tk()
root.title("Tic-Tac-Toe")
buttons = [[None for _ in range(3)] for _ in range(3)]

for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(root, text="", font=('Arial', 40), width=5, height=2,
                                  command=lambda i=i,j=j: click(i,j))
        buttons[i][j].grid(row=i, column=j)

result_label = tk.Label(root, text="", font=('Arial', 20))
result_label.grid(row=3, column=0, columnspan=3)

reset_button = tk.Button(root, text="Reset", font=('Arial', 15), command=reset)
reset_button.grid(row=4, column=0, columnspan=3)

root.mainloop()
