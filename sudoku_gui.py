import random, copy
import tkinter as tk
from tkinter import messagebox

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver with Difficulty & Hints")
        self.root.configure(bg="#2e2e2e")
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.solution = [[0]*9 for _ in range(9)]
        self.create_grid()
        self.create_buttons()

    def create_grid(self):
        for row in range(9):
            for col in range(9):
                entry = tk.Entry(self.root, width=2, font=('Arial', 18), justify='center',
                                 bg="#3c3f41", fg="white", insertbackground='white')
                entry.grid(row=row, column=col, padx=1, pady=1)
                self.cells[row][col] = entry

    def create_buttons(self):
        tk.Button(self.root, text="Solve", command=self.solve, bg="#4caf50", fg="white").grid(row=9, column=0, columnspan=2, sticky="nsew")
        tk.Button(self.root, text="Clear", command=self.clear_grid, bg="#f44336", fg="white").grid(row=9, column=2, columnspan=2, sticky="nsew")
        tk.Button(self.root, text="Hint", command=self.give_hint, bg="#ff9800", fg="white").grid(row=9, column=4, columnspan=2, sticky="nsew")
        tk.Button(self.root, text="Easy", command=lambda: self.generate_puzzle(45), bg="#2196f3", fg="white").grid(row=9, column=6, sticky="nsew")
        tk.Button(self.root, text="Med", command=lambda: self.generate_puzzle(35), bg="#3f51b5", fg="white").grid(row=9, column=7, sticky="nsew")
        tk.Button(self.root, text="Hard", command=lambda: self.generate_puzzle(25), bg="#673ab7", fg="white").grid(row=9, column=8, sticky="nsew")

    def clear_grid(self):
        for row in range(9):
            for col in range(9):
                self.cells[row][col].delete(0, tk.END)

    def get_board(self):
        board = []
        for row in range(9):
            row_vals = []
            for col in range(9):
                val = self.cells[row][col].get()
                if val == '':
                    row_vals.append(0)
                else:
                    try:
                        row_vals.append(int(val))
                    except ValueError:
                        messagebox.showerror("Invalid input", "Use numbers 1–9 only.")
                        return None
            board.append(row_vals)
        return board

    def set_board(self, board):
        for row in range(9):
            for col in range(9):
                self.cells[row][col].delete(0, tk.END)
                if board[row][col] != 0:
                    self.cells[row][col].insert(0, str(board[row][col]))

    def is_valid(self, board, row, col, num):
        for x in range(9):
            if board[row][x] == num or board[x][col] == num:
                return False
        start_row, start_col = row - row % 3, col - col % 3
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        return True

    def solve_sudoku(self, board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid(board, row, col, num):
                            board[row][col] = num
                            if self.solve_sudoku(board):
                                return True
                            board[row][col] = 0
                    return False
        return True

    def solve(self):
        board = self.get_board()
        if board and self.solve_sudoku(board):
            self.set_board(board)
        else:
            messagebox.showinfo("Result", "No solution exists!")

    def generate_puzzle(self, filled_cells):
        # Start with an empty board and solve it to get a complete board
        board = [[0]*9 for _ in range(9)]
        self.solve_sudoku(board)
        self.solution = copy.deepcopy(board)

        # Remove cells to match difficulty
        count = 81 - filled_cells
        while count > 0:
            r, c = random.randint(0, 8), random.randint(0, 8)
            if board[r][c] != 0:
                board[r][c] = 0
                count -= 1

        self.set_board(board)

    def give_hint(self):
        current_board = self.get_board()
        if not self.solution or not any(0 in row for row in current_board):
            messagebox.showinfo("Hint", "Nothing to hint.")
            return

        for row in range(9):
            for col in range(9):
                if current_board[row][col] == 0:
                    self.cells[row][col].insert(0, str(self.solution[row][col]))
                    return

# Launch GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
