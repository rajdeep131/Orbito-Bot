import tkinter as tk
from tkinter import messagebox

class OrbitoGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Orbito Game")

        # Initialize the game board (4x4)
        self.board = [[None for _ in range(4)] for _ in range(4)]
        self.current_player = "Player 1"  # Alternates between Player 1 and Player 2
        self.colors = {"Player 1": "black", "Player 2": "white"}
        self.opponent_move_mode = False  # Track if the player is moving an opponent's piece
        self.selected_opponent_piece = None  # The selected opponent piece to move

        # Create GUI components
        self.create_board()
        self.create_controls()

    def create_board(self):
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="lightgray")
        self.canvas.pack(side=tk.TOP)

        # Draw the grid
        for i in range(5):
            self.canvas.create_line(0, i * 100, 400, i * 100, fill="black")
            self.canvas.create_line(i * 100, 0, i * 100, 400, fill="black")

        # Add click handler
        self.canvas.bind("<Button-1>", self.handle_click)

    def create_controls(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.turn_label = tk.Label(control_frame, text=f"Turn: {self.current_player}", font=("Arial", 14))
        self.turn_label.pack(side=tk.LEFT, padx=10)

        reset_button = tk.Button(control_frame, text="Reset", command=self.reset_game)
        reset_button.pack(side=tk.RIGHT, padx=10)

    def handle_click(self, event):
        x, y = event.x // 100, event.y // 100

        if self.opponent_move_mode:
            # If in opponent's move mode, move their piece
            if self.move_opponent_piece(x, y):
                self.opponent_move_mode = False
                self.selected_opponent_piece = None
                self.redraw_board()
            else:
                messagebox.showerror("Invalid Move", "Invalid position to move the opponent's piece!")
            return

        # Check if the player clicked on an opponent's piece
        if self.board[y][x] is not None and self.board[y][x] != self.colors[self.current_player]:
            self.highlight_valid_moves(x, y)
            self.selected_opponent_piece = (x, y)
            self.opponent_move_mode = True
            return

        # Place the current player's piece if the clicked cell is empty
        if self.board[y][x] is None:
            self.board[y][x] = self.colors[self.current_player]
            self.draw_marble(x, y, self.colors[self.current_player])

            # Pause for 300ms before rotating
            self.root.after(300, self.rotate_after_pause)

            # Switch turn
            self.current_player = "Player 2" if self.current_player == "Player 1" else "Player 1"
            self.turn_label.config(text=f"Turn: {self.current_player}")

    def rotate_after_pause(self):
        """Rotate the board after a short pause."""
        self.rotate_board()

    def highlight_valid_moves(self, x, y):
        """Highlight valid positions where the selected opponent's piece can move."""
        neighbors = [
            (x, y - 1),  # Up
            (x, y + 1),  # Down
            (x - 1, y),  # Left
            (x + 1, y)   # Right
        ]
        self.redraw_board()  # Clear any existing highlights

        for nx, ny in neighbors:
            if 0 <= nx < 4 and 0 <= ny < 4 and self.board[ny][nx] is None:
                cx, cy = nx * 100 + 50, ny * 100 + 50
                self.canvas.create_rectangle(
                    cx - 40, cy - 40, cx + 40, cy + 40, fill="yellow", outline="black", tags="highlight"
                )

    def move_opponent_piece(self, x, y):
        """Move the opponent's selected piece to a new position."""
        if self.selected_opponent_piece is None:
            return False

        ox, oy = self.selected_opponent_piece
        neighbors = [
            (ox, oy - 1),  # Up
            (ox, oy + 1),  # Down
            (ox - 1, oy),  # Left
            (ox + 1, oy)   # Right
        ]

        if (x, y) in neighbors and self.board[y][x] is None:
            self.board[y][x] = self.board[oy][ox]
            self.board[oy][ox] = None
            return True

        return False

    def draw_marble(self, x, y, color):
        cx, cy = x * 100 + 50, y * 100 + 50
        self.canvas.create_oval(cx - 30, cy - 30, cx + 30, cy + 30, fill=color, outline="black")

    def rotate_board(self):
        """Perform a single-step adjacent rotation counterclockwise."""
        new_board = [[None for _ in range(4)] for _ in range(4)]

        outer_positions = [
            (0, i) for i in range(4)
        ] + [
            (i, 3) for i in range(1, 4)
        ] + [
            (3, i) for i in range(2, -1, -1)
        ] + [
            (i, 0) for i in range(2, 0, -1)
        ]

        inner_positions = [
            (1, 1), (1, 2), (2, 2), (2, 1)
        ]

        for i, (y, x) in enumerate(outer_positions):
            ny, nx = outer_positions[(i - 1) % len(outer_positions)]
            new_board[ny][nx] = self.board[y][x]

        for i, (y, x) in enumerate(inner_positions):
            ny, nx = inner_positions[(i - 1) % len(inner_positions)]
            new_board[ny][nx] = self.board[y][x]

        self.board = new_board
        self.redraw_board()

    def redraw_board(self):
        self.canvas.delete("all")
        for i in range(5):
            self.canvas.create_line(0, i * 100, 400, i * 100, fill="black")
            self.canvas.create_line(i * 100, 0, i * 100, 400, fill="black")

        for y in range(4):
            for x in range(4):
                if self.board[y][x] is not None:
                    self.draw_marble(x, y, self.board[y][x])

    def reset_game(self):
        self.board = [[None for _ in range(4)] for _ in range(4)]
        self.current_player = "Player 1"
        self.opponent_move_mode = False
        self.selected_opponent_piece = None
        self.turn_label.config(text=f"Turn: {self.current_player}")
        self.redraw_board()

if __name__ == "__main__":
    root = tk.Tk()
    game = OrbitoGame(root)
    root.mainloop()
