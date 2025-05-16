import tkinter as tk
from tkinter import messagebox
import random
import math

# -----------------------------
# Global Constants for Board UI
# -----------------------------
ROW_COUNT = 6
COLUMN_COUNT = 7
TOP_MARGIN = 40  # Extra space at top for column numbers

# Use classic Connect 4 colors:
# PLAYER_PIECE will be red, AI_PIECE will be yellow.
PLAYER_PIECE = 1
AI_PIECE = 2
EMPTY = 0

# -----------------------------
# Game Logic Functions
# -----------------------------
def create_board():
    return [[EMPTY for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[0][col] == EMPTY

def get_valid_locations(board):
    return [col for col in range(COLUMN_COUNT) if is_valid_location(board, col)]

def get_next_open_row(board, col):
    for r in range(ROW_COUNT - 1, -1, -1):
        if board[r][col] == EMPTY:
            return r

def winning_move(board, piece):
    # Check horizontal locations for win.
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if all(board[r][c+i] == piece for i in range(4)):
                return True
    # Check vertical locations for win.
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True
    # Check positively sloped diagonals.
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True
    # Check negatively sloped diagonals.
    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True
    return False

def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4
    return score

def score_position(board, piece):
    score = 0
    # Score center column.
    center = [board[r][COLUMN_COUNT // 2] for r in range(ROW_COUNT)]
    score += center.count(piece) * 3

    # Score Horizontal.
    for r in range(ROW_COUNT):
        row_array = board[r]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c+4]
            score += evaluate_window(window, piece)

    # Score Vertical.
    for c in range(COLUMN_COUNT):
        col_array = [board[r][c] for r in range(ROW_COUNT)]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r+4]
            score += evaluate_window(window, piece)

    # Score positive diagonal.
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Score negative diagonal.
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+3-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer, piece):
    valid_locations = get_valid_locations(board)
    terminal = is_terminal_node(board)
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    if depth == 0 or terminal:
        if terminal:
            if winning_move(board, piece):
                return (None, 100000000000000)
            elif winning_move(board, opp_piece):
                return (None, -10000000000000)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, piece))
    
    if maximizingPlayer:
        value = -math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            board_copy = [r[:] for r in board]
            drop_piece(board_copy, row, col, piece)
            new_score = minimax(board_copy, depth-1, alpha, beta, False, piece)[1]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value
    else:
        value = math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            board_copy = [r[:] for r in board]
            drop_piece(board_copy, row, col, opp_piece)
            new_score = minimax(board_copy, depth-1, alpha, beta, True, piece)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value

# -----------------------------
# Strategy Helper Functions
# -----------------------------
def get_move_explanation(board, move_col, piece):
    """
    Provides strategic reasoning for move suggestions:
      - If the move blocks an opponent's winning move, highlight this defensive strategy
      - If the move is in the centre column, explain the positional advantage
      - Otherwise, explain based on win probability
    """
    opp_piece = AI_PIECE if piece == PLAYER_PIECE else PLAYER_PIECE
    # Check for immediate opponent threat.
    for col in get_valid_locations(board):
        row = get_next_open_row(board, col)
        board_copy = [r[:] for r in board]
        drop_piece(board_copy, row, col, opp_piece)
        if winning_move(board_copy, opp_piece):
            if move_col == col:
                return f"(Blocks an immediate winning move for your opponent)"
    # Check if move is in the center.
    center = COLUMN_COUNT // 2
    if move_col == center:
        return f"(Central position to maximise your control of the board)"    # Default explanation.
    return f"(highest calculated win probability)"

# -----------------------------
# Tkinter GUI Implementation
# -----------------------------
class Connect4App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Connect 4")
        self.resizable(False, False)
        self.configure(bg="lightblue")
        self.container = tk.Frame(self, bg="lightblue")
        self.container.pack(side="top", fill="both", expand=True)
        self.frames = {}

        for F in (WelcomeFrame, GameFrame):
            frame = F(parent=self.container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(WelcomeFrame)

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()

    def start_game(self, mode, difficulty):
        game_frame = self.frames[GameFrame]
        game_frame.new_game(mode, difficulty)
        self.show_frame(GameFrame)

class WelcomeFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="lightblue")
        self.controller = controller

        title = tk.Label(self, text="Welcome to Connect 4!", font=("Helvetica", 24, "bold"), bg="lightblue")
        title.pack(pady=20)        # Game mode selection
        mode_label = tk.Label(self, text="Select Game Mode:", font=("Helvetica", 14), bg="lightblue")
        mode_label.pack(pady=5)
        self.mode_var = tk.StringVar(value="Human vs AI")
        mode_options = ["Human vs AI", "Human vs Human", "AI vs AI", "Assisted"]
        self.mode_menu = tk.OptionMenu(self, self.mode_var, *mode_options, command=self.mode_changed)
        self.mode_menu.config(font=("Helvetica", 12))
        self.mode_menu.pack()

        self.difficulty_label = tk.Label(self, text="Select AI Difficulty:", font=("Helvetica", 14), bg="lightblue")
        self.difficulty_label.pack(pady=5)
        self.difficulty_var = tk.StringVar(value="Medium")
        difficulty_options = ["Easy", "Medium", "Hard"]
        self.difficulty_menu = tk.OptionMenu(self, self.difficulty_var, *difficulty_options)
        self.difficulty_menu.config(font=("Helvetica", 12))
        self.difficulty_menu.pack()

        start_button = tk.Button(self, text="Start Game", font=("Helvetica", 14), command=self.start_game)
        start_button.pack(pady=20)

    def mode_changed(self, value):
        # Disable AI difficulty when playing Human vs Human.
        if value == "Human vs Human":
            self.difficulty_menu.configure(state="disabled")
            self.difficulty_label.configure(state="disabled")
        else:
            self.difficulty_menu.configure(state="normal")
            self.difficulty_label.configure(state="normal")

    def start_game(self):
        mode = self.mode_var.get()
        difficulty = self.difficulty_var.get()
        self.controller.start_game(mode, difficulty)

class GameFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="lightblue")
        self.controller = controller

        self.board = create_board()
        self.game_over = False
        self.mode = "Human vs AI"
        self.ai_depth = 5
        self.turn = None

        self.cell_size = 100
        self.canvas_width = COLUMN_COUNT * self.cell_size
        # Increase height to add TOP_MARGIN for column numbers.
        self.canvas_height = ROW_COUNT * self.cell_size + TOP_MARGIN
        # Deep blue background to mimic a Connect 4 board.
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, bg="blue", highlightthickness=0)
        self.canvas.pack(padx=20, pady=20)
        self.canvas.bind("<Button-1>", self.click_handler)

        # A label to display the suggestion/hint in Assisted mode.
        # The wraplength ensures the hint text wraps without expanding the window.
        self.hint_label = tk.Label(self, text="", font=("Helvetica", 14), bg="lightblue", wraplength=400)
        self.hint_label.pack(pady=5)

        self.restart_button = tk.Button(self, text="Restart", font=("Helvetica", 14), command=self.restart)
        self.restart_button.pack(pady=10)

    def new_game(self, mode, difficulty):
        self.mode = mode
        if difficulty == "Easy":
            self.ai_depth = 3
        elif difficulty == "Medium":
            self.ai_depth = 5
        elif difficulty == "Hard":
            self.ai_depth = 7

        self.board = create_board()
        self.game_over = False
        # For Human vs Human and Assisted mode, human (red) always starts.
        if self.mode in ["Human vs Human", "Assisted"]:
            self.turn = PLAYER_PIECE
        else:
            self.turn = random.choice([PLAYER_PIECE, AI_PIECE])
        self.draw_board()
        self.hint_label.config(text="")  # Clear any previous hints.

        # Schedule AI move if needed.
        if ((self.mode in ["Human vs AI", "Assisted"]) and self.turn == AI_PIECE) or self.mode == "AI vs AI":
            self.after(1000, self.ai_move)
        # In Assisted mode, update the hint if it's the human’s turn.
        if self.mode == "Assisted" and self.turn == PLAYER_PIECE:
            self.after(500, self.update_hint)

    def restart(self):
        self.controller.show_frame(WelcomeFrame)

    def draw_board(self):
        self.canvas.delete("all")
        # Draw column numbers in the TOP_MARGIN area.
        for c in range(COLUMN_COUNT):
            x = c * self.cell_size + self.cell_size / 2
            y = TOP_MARGIN / 2
            self.canvas.create_text(x, y, text=str(c), fill="white", font=("Helvetica", 16, "bold"))

        # Draw empty slots and pieces, shifting y-coordinates by TOP_MARGIN.
        for r in range(ROW_COUNT):
            for c in range(COLUMN_COUNT):
                x1 = c * self.cell_size + 5
                y1 = TOP_MARGIN + r * self.cell_size + 5
                x2 = (c+1) * self.cell_size - 5
                y2 = TOP_MARGIN + (r+1) * self.cell_size - 5
                self.canvas.create_oval(x1, y1, x2, y2, fill="white", outline="black")
        for r in range(ROW_COUNT):
            for c in range(COLUMN_COUNT):
                if self.board[r][c] != EMPTY:
                    color = "red" if self.board[r][c] == PLAYER_PIECE else "yellow"
                    x1 = c * self.cell_size + 5
                    y1 = TOP_MARGIN + r * self.cell_size + 5
                    x2 = (c+1) * self.cell_size - 5
                    y2 = TOP_MARGIN + (r+1) * self.cell_size - 5
                    self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline="black")

    def animate_piece_drop(self, row, col, piece, callback=None):
        """Animate a piece dropping from the top into the desired cell."""
        color = "red" if piece == PLAYER_PIECE else "yellow"
        x1 = col * self.cell_size + 5
        x2 = (col+1) * self.cell_size - 5
        final_y = TOP_MARGIN + row * self.cell_size + 5
        current_y = -self.cell_size  # Start above the board.
        piece_id = self.canvas.create_oval(x1, current_y, x2, current_y + self.cell_size - 10, fill=color, outline="black")

        def drop_step():
            nonlocal current_y
            step = 20
            if current_y < final_y:
                self.canvas.move(piece_id, 0, step)
                current_y += step
                self.after(20, drop_step)
            else:
                self.canvas.delete(piece_id)
                self.draw_board()
                if callback:
                    callback()
        drop_step()

    def after_move(self):
        """Called after an animated move; checks for win/draw and switches turns."""
        if winning_move(self.board, self.turn):
            self.game_over = True
            winner = "Red" if self.turn == PLAYER_PIECE else "Yellow"
            messagebox.showinfo("Game Over", f"{winner} wins!")
            self.hint_label.config(text="")
            return
        if len(get_valid_locations(self.board)) == 0:
            self.game_over = True
            messagebox.showinfo("Game Over", "It's a draw!")
            self.hint_label.config(text="")
            return

        # Switch turn.
        self.turn = AI_PIECE if self.turn == PLAYER_PIECE else PLAYER_PIECE

        # Schedule AI move if it's AI's turn.
        if ((self.mode in ["Human vs AI", "Assisted"]) and self.turn == AI_PIECE) or self.mode == "AI vs AI":
            self.after(1000, self.ai_move)
        # In Assisted mode, update the hint when it becomes the human’s turn.
        if self.mode == "Assisted" and self.turn == PLAYER_PIECE:
            self.after(500, self.update_hint)
        else:
            self.hint_label.config(text="")

    def click_handler(self, event):
        if self.game_over:
            return
        # Determine which column was clicked (ignore y-coordinate since numbers are at top).
        col = event.x // self.cell_size
        # In Human vs AI and Assisted modes, process clicks only if it's the human's turn.
        if self.mode in ["Human vs AI", "Assisted"] and self.turn != PLAYER_PIECE:
            return
        if self.mode in ["Human vs AI", "Human vs Human", "Assisted"]:
            self.human_move(col)

    def human_move(self, col):
        if not is_valid_location(self.board, col):
            messagebox.showwarning("Invalid Move", "Column is full!")
            return
        row = get_next_open_row(self.board, col)
        drop_piece(self.board, row, col, self.turn)
        self.animate_piece_drop(row, col, self.turn, callback=self.after_move)

    def ai_move(self):
        if self.game_over:
            return
        piece = self.turn
        col, _ = minimax(self.board, self.ai_depth, -math.inf, math.inf, True, piece)
        if col is None or not is_valid_location(self.board, col):
            return
        row = get_next_open_row(self.board, col)
        drop_piece(self.board, row, col, piece)
        self.animate_piece_drop(row, col, piece, callback=self.after_move)

    def update_hint(self):
        """
        Calculates and displays strategic move suggestions in Assisted mode.
        Uses minimax algorithm to evaluate possible moves and presents the best option
        with a win probability percentage and strategic explanation.
        """
        if self.mode != "Assisted" or self.game_over or self.turn != PLAYER_PIECE:
            self.hint_label.config(text="")
            return

        # Immediately inform the user that the system is "Thinking..."
        self.hint_label.config(text="Thinking...")
        self.hint_label.update()  # Force an update so the user sees "Thinking..."

        valid_moves = get_valid_locations(self.board)
        if not valid_moves:
            self.hint_label.config(text="No moves available")
            return

        suggestion_depth = 5
        scores = {}
        for col in valid_moves:
            row = get_next_open_row(self.board, col)
            board_copy = [r[:] for r in self.board]
            drop_piece(board_copy, row, col, PLAYER_PIECE)
            _, score = minimax(board_copy, suggestion_depth, -math.inf, math.inf, False, PLAYER_PIECE)
            scores[col] = score

        max_score = max(scores.values())
        exp_values = {col: math.exp(scores[col] - max_score) for col in scores}
        sum_exp = sum(exp_values.values())
        probabilities = {col: exp_values[col] / sum_exp for col in exp_values}
        best_col = max(probabilities, key=probabilities.get)
        best_prob = probabilities[best_col] * 100
        explanation = get_move_explanation(self.board, best_col, PLAYER_PIECE)
        hint_text = f"Hint: Try column {best_col} (Win chance: {best_prob:.1f}%). {explanation}"
        self.hint_label.config(text=hint_text)

# -----------------------------
# Run the Application
# -----------------------------
if __name__ == "__main__":
    app = Connect4App()
    app.mainloop()
