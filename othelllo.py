import tkinter as tk
from tkinter import messagebox
import copy

class OthelloGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Othello Game")
        self.master.resizable(False, False)
        
        # Create game instance
        self.game = Othello()
        self.board = copy.deepcopy(self.game.board)
        
        # Game colors
        self.bg_color = "#27ae60"  # Green background
        self.grid_color = "#2ecc71"  # Lighter green for grid
        self.black_color = "#2c3e50"  # Dark for X (Computer)
        self.white_color = "#ecf0f1"  # Light for O (Human)
        self.valid_move_color = "#f1c40f"  # Yellow for valid moves
        
        # Create UI elements
        self.create_widgets()
        
        # Start game
        self.update_display()
        self.highlight_valid_moves()
        
    def create_widgets(self):
        # Top frame for scores and turn indicator
        top_frame = tk.Frame(self.master)
        top_frame.pack(pady=10)
        
        self.score_label = tk.Label(top_frame, text="Score: X: 2 | O: 2", font=("Arial", 14))
        self.score_label.pack(side=tk.LEFT, padx=20)
        
        self.turn_label = tk.Label(top_frame, text="Your Turn (O)", font=("Arial", 14))
        self.turn_label.pack(side=tk.RIGHT, padx=20)
        
        # Canvas for the game board
        self.canvas_size = 600
        self.cell_size = self.canvas_size // 8
        self.canvas = tk.Canvas(self.master, width=self.canvas_size, height=self.canvas_size, bg=self.bg_color)
        self.canvas.pack(padx=10, pady=10)
        
        # Draw grid
        self.draw_grid()
        
        # Bottom frame for buttons
        bottom_frame = tk.Frame(self.master)
        bottom_frame.pack(pady=10)
        
        self.new_game_button = tk.Button(bottom_frame, text="New Game", command=self.new_game, font=("Arial", 12))
        self.new_game_button.pack(side=tk.LEFT, padx=10)
        
        self.pass_button = tk.Button(bottom_frame, text="Pass Turn", command=self.pass_turn, font=("Arial", 12))
        self.pass_button.pack(side=tk.LEFT, padx=10)
        
        # Bind click event
        self.canvas.bind("<Button-1>", self.on_click)
        
        # Valid move indicators
        self.valid_indicators = []
        
    def draw_grid(self):
        # Draw grid lines
        for i in range(9):
            # Vertical lines
            x = i * self.cell_size
            self.canvas.create_line(x, 0, x, self.canvas_size, width=2, fill=self.grid_color)
            # Horizontal lines
            y = i * self.cell_size
            self.canvas.create_line(0, y, self.canvas_size, y, width=2, fill=self.grid_color)
    
    def update_display(self):
        # Clear canvas except grid
        self.canvas.delete("disc")
        self.canvas.delete("indicator")
        
        # Draw discs
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == 'X':  # Computer (black)
                    self.draw_disc(r, c, self.black_color)
                elif self.board[r][c] == 'O':  # Human (white)
                    self.draw_disc(r, c, self.white_color)
        
        # Update scores
        x_count = sum(row.count('X') for row in self.board)
        o_count = sum(row.count('O') for row in self.board)
        self.score_label.config(text=f"Score: X: {x_count} | O: {o_count}")
        
        # Check if game is over
        if self.game.terminal(self.board):
            self.game_over()
    
    def draw_disc(self, row, col, color):
        x1 = col * self.cell_size + 10
        y1 = row * self.cell_size + 10
        x2 = (col + 1) * self.cell_size - 10
        y2 = (row + 1) * self.cell_size - 10
        self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline="black", width=2, tags="disc")
    
    def highlight_valid_moves(self):
        # Clear previous indicators
        self.canvas.delete("indicator")
        
        # Get valid moves for human player
        moves = self.game.valid_moves(self.board, 'O')
        
        # Draw indicators for valid moves
        for r, c in moves:
            x = c * self.cell_size + self.cell_size // 2
            y = r * self.cell_size + self.cell_size // 2
            radius = 8
            self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, 
                                   fill=self.valid_move_color, outline="", tags="indicator")
    
    def on_click(self, event):
        # Calculate row and column from click position
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        
        # Check if it's human's turn
        if not self.is_human_turn():
            return
        
        # Check if move is valid
        moves = self.game.valid_moves(self.board, 'O')
        if (row, col) not in moves:
            return
        
        # Make the move
        self.board = self.game.make_move(self.board, row, col, 'O')
        self.update_display()
        
        # Check if game is over
        if self.game.terminal(self.board):
            return
        
        # Check if computer has valid moves
        if not self.game.valid_moves(self.board, 'X'):
            messagebox.showinfo("No Moves", "Computer has no valid moves. Your turn again.")
            self.highlight_valid_moves()
            return
        
        # Update turn indicator
        self.turn_label.config(text="Computer's Turn (X)")
        
        # Make computer move after a short delay
        self.master.after(1000, self.computer_move)
    
    def computer_move(self):
        # Make computer move
        self.board = self.game.computer_move(self.board)
        self.update_display()
        
        # Check if game is over
        if self.game.terminal(self.board):
            return
        
        # Check if human has valid moves
        if not self.game.valid_moves(self.board, 'O'):
            messagebox.showinfo("No Moves", "You have no valid moves. Computer's turn again.")
            self.master.after(1000, self.computer_move)
            return
        
        # Update turn indicator and highlight valid moves
        self.turn_label.config(text="Your Turn (O)")
        self.highlight_valid_moves()
    
    def is_human_turn(self):
        # Check if it's human's turn based on the turn label
        return "Your Turn" in self.turn_label.cget("text")
    
    def pass_turn(self):
        if not self.is_human_turn():
            messagebox.showinfo("Not Your Turn", "It's not your turn to pass.")
            return
        
        # Check if player has valid moves
        if self.game.valid_moves(self.board, 'O'):
            messagebox.showinfo("Valid Moves", "You have valid moves. You cannot pass.")
            return
        
        # Pass turn
        self.turn_label.config(text="Computer's Turn (X)")
        self.master.after(1000, self.computer_move)
    
    def game_over(self):
        # Count discs
        x_count = sum(row.count('X') for row in self.board)
        o_count = sum(row.count('O') for row in self.board)
        
        # Determine winner
        if x_count > o_count:
            message = f"Computer wins!\nFinal Score -> X: {x_count} | O: {o_count}"
        elif x_count < o_count:
            message = f"You win!\nFinal Score -> X: {x_count} | O: {o_count}"
        else:
            message = f"It's a draw!\nFinal Score -> X: {x_count} | O: {o_count}"
        
        # Show game over dialog
        result = messagebox.showinfo("Game Over", message)
        
        # Ask if player wants to play again
        play_again = messagebox.askyesno("Play Again", "Do you want to play another game?")
        if play_again:
            self.new_game()
    
    def new_game(self):
        # Reset game
        self.game = Othello()
        self.board = copy.deepcopy(self.game.board)
        
        # Update display
        self.update_display()
        self.highlight_valid_moves()
        
        # Reset turn indicator
        self.turn_label.config(text="Your Turn (O)")


class Othello:
    def __init__(self):
        # Create 8x8 board
        self.board = [
  [" "," "," "," "," "," "," "," "], 
  [" "," "," "," "," "," "," "," "], 
  [" "," "," "," "," "," "," "," "], 
  [" "," "," "," "," "," "," "," "], 
  [" "," "," "," "," "," "," "," "],  
  [" "," "," "," "," "," "," "," "],  
  [" "," "," "," "," "," "," "," "], 
  [" "," "," "," "," "," "," "," "]  ]
        # Initial 4 discs in the center
        self.board[3][3] = 'O'
        self.board[3][4] = 'X'
        self.board[4][3] = 'X'
        self.board[4][4] = 'O'


    # Get opponent
    def opponent(self, player):
        return 'O' if player == 'X' else 'X'

    # Check if move is valid
    def valid_moves(self, board, player):
        moves = []
        for r in range(8):
            for c in range(8):
                if board[r][c] == " " and self.can_flip(board, r, c, player):
                    moves.append((r, c))
        return moves

    # Check if a move can flip any opponent discs
    def can_flip(self, board, row, col, player):
        directions = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
        opponent = self.opponent(player)
        for dr, dc in directions:
            r, c = row+dr, col+dc
            found_opponent = False
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] == opponent:
                    found_opponent = True
                elif board[r][c] == player:
                    if found_opponent:
                        return True
                    else:
                        break
                else:
                    break
                r += dr
                c += dc
        return False

    # Apply move
    def make_move(self, board, row, col, player):
        new_board = copy.deepcopy(board)
        new_board[row][col] = player
        self.flip_discs(new_board, row, col, player)
        return new_board

    # Flip discs after move
    def flip_discs(self, board, row, col, player):
        directions = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
        opponent = self.opponent(player)
        for dr, dc in directions:
            r, c = row+dr, col+dc
            discs_to_flip = []
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] == opponent:
                    discs_to_flip.append((r,c))
                elif board[r][c] == player:
                    for fr, fc in discs_to_flip:
                        board[fr][fc] = player
                    break
                else:
                    break
                r += dr
                c += dc

    # Check if game is over
    def terminal(self, board):
        return not self.valid_moves(board, 'X') and not self.valid_moves(board, 'O')

    # Evaluate board for MinMax
    def evaluate(self, board, player):
        x_count = sum(row.count('X') for row in board)
        o_count = sum(row.count('O') for row in board)
        return x_count - o_count if player == 'X' else o_count - x_count

    # MinMax with Alpha-Beta Pruning
    def MinMax(self, board, depth, player, alpha, beta):
        if depth == 0 or self.terminal(board):
            return self.evaluate(board, player)

        moves = self.valid_moves(board, player)
        if not moves:
            return self.MinMax(board, depth-1, self.opponent(player), alpha, beta)

        if player == 'X':  # Max player
            max_eval = float('-inf')
            for r, c in moves:
                next_board = self.make_move(board, r, c, player)
                eval = self.MinMax(next_board, depth-1, 'O', alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:  # Min player
            min_eval = float('inf')
            for r, c in moves:
                next_board = self.make_move(board, r, c, player)
                eval = self.MinMax(next_board, depth-1, 'X', alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    # Computer move
    def computer_move(self, board):
        moves = self.valid_moves(board, 'X')
        if not moves:
            return board

        best_val = float('-inf')
        best_move = None
        for r, c in moves:
            next_board = self.make_move(board, r, c, 'X')
            val = self.MinMax(next_board, 3, 'O', float('-inf'), float('inf'))
            if val > best_val:
                best_val = val
                best_move = (r, c)

        new_board = self.make_move(board, best_move[0], best_move[1], 'X')
        return new_board


# Main function to run the game
if __name__ == "__main__":
    root = tk.Tk()
    app = OthelloGUI(root)
    root.mainloop()