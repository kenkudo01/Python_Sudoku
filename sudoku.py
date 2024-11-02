import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt

class Board:
    def __init__(self):
        
        self.board = [[None for _ in range(9)] for _ in range(9)]

    def set_value(self, row, col, value):
 
        self.board[row][col] = value

    def get_value(self, row, col):
  
        return self.board[row][col]

    def is_cell_valid(self, row, col):
     
        num = self.get_value(row, col)
        if num is None:
            return False

     
        for i in range(9):
            if i != col and self.get_value(row, i) == num:
                return False

       
        for i in range(9):
            if i != row and self.get_value(i, col) == num:
                return False

       
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                r = start_row + i
                c = start_col + j
                if (r != row or c != col) and self.get_value(r, c) == num:
                    return False

        return True

    def is_board_filled(self):
     
        for row in range(9):
            for col in range(9):
                if self.get_value(row, col) is None:
                    return False
        return True

class Algorithm2Solver:
    def __init__(self, board, cells):
        self.board = board
        self.cells = cells

    def solve(self):
        start_time = time.time()
        solved = self.solve_recursive()
        end_time = time.time()
        solve_time = end_time - start_time
        return solved, solve_time

    def find_next_cell(self):
        min_candidates = 10
        next_cell = None
        for row in range(9):
            for col in range(9):
                if self.board.get_value(row, col) is None:
                    candidates = self.get_candidates(row, col)
                    if len(candidates) < min_candidates:
                        min_candidates = len(candidates)
                        next_cell = (row, col, candidates)
                    if min_candidates == 1:
                        return next_cell
        return next_cell

    def get_candidates(self, row, col):
        used_numbers = set()
      
        for c in range(9):
            num = self.board.get_value(row, c)
            if num:
                used_numbers.add(num)
     
        for r in range(9):
            num = self.board.get_value(r, col)
            if num:
                used_numbers.add(num)
 
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(3):
            for c in range(3):
                num = self.board.get_value(start_row + r, start_col + c)
                if num:
                    used_numbers.add(num)
        return set(range(1, 10)) - used_numbers

    def solve_recursive(self):
        cell = self.find_next_cell()
        if not cell:
            return True 
        row, col, candidates = cell
        for num in candidates:
            self.board.set_value(row, col, num)
            self.cells[(row, col)].setText(str(num))
            QApplication.processEvents()

            if self.solve_recursive():
                return True

            self.board.set_value(row, col, None)
            self.cells[(row, col)].clear()
        return False

    
    
        

class Algorithm1Solver:
    def __init__(self, board, cells):
        self.board = board
        self.cells = cells

    def solve(self):
        start_time = time.time()
        solved = self.solve_recursive()
        end_time = time.time()
        solve_time = end_time - start_time
        return solved, solve_time

    def solve_recursive(self):
        for row in range(9):
            for col in range(9):
                if self.board.get_value(row, col) is None:
                    for num in range(1, 10):
                        self.board.set_value(row, col, num)
                        self.cells[(row, col)].setText(str(num))
                        QApplication.processEvents()

                        if self.board.is_cell_valid(row, col) and self.solve_recursive():
                            return True

                        self.board.set_value(row, col, None)
                        self.cells[(row, col)].clear()
                    return False
        return True

class SudokuSolverApp(QWidget):
    def __init__(self):
        super().__init__()
        self.board = Board() 
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Sudoku Solver')
        self.setGeometry(100, 100, 450, 750)
        self.setFixedSize(450, 750)
        self.setStyleSheet("""
            background-color: black;
            font-family: 'Roboto', sans-serif;
            color: white;
        """)

        layout = QVBoxLayout()

        self.grid = QGridLayout()
        self.cells = {}
        validator = QIntValidator(1, 9)

        for row in range(9):
            for col in range(9):
                cell = QLineEdit(self)
                cell.setMaxLength(1)
                cell.setValidator(validator)
                cell.setFixedSize(40, 40)
                cell.setAlignment(Qt.AlignCenter)
                self.set_cell_style(cell, row, col)
                cell.textChanged.connect(lambda text, r=row, c=col: self.update_board(r, c, text))


                grid_row = row + (row // 3)
                grid_col = col + (col // 3)
                self.grid.addWidget(cell, grid_row, grid_col)

                self.cells[(row, col)] = cell

        layout.addLayout(self.grid)

        input_layout = QHBoxLayout()
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Enter 81 digits (0 for empty cells)")
        self.input_field.setStyleSheet("""
            background-color: #444444; 
            color: white; 
            padding: 5px; 
            border-radius: 5px; 
            font-family: 'Roboto', sans-serif;
            font-size: 14px;
        """)
        input_layout.addWidget(self.input_field)

        apply_button = QPushButton('Apply Input', self)
        apply_button.clicked.connect(self.apply_input_to_board)
        apply_button.setStyleSheet("""
            background-color: #555555; 
            color: white; 
            padding: 5px; 
            border-radius: 5px;
            font-family: 'Roboto', sans-serif;
            font-size: 14px;
        """)
        input_layout.addWidget(apply_button)

        layout.addLayout(input_layout)

        solve_button = QPushButton('Solve', self)
        solve_button.clicked.connect(self.solve_sudoku)
        solve_button.setStyleSheet("""
            background-color: #555555; 
            color: white; 
            padding: 5px; 
            border-radius: 5px;
            font-family: 'Roboto', sans-serif;
            font-size: 14px;
        """)
        layout.addWidget(solve_button)
        
        solve_button2 = QPushButton('optimize', self)
        solve_button2.clicked.connect(self.solve_sudoku2)
        solve_button2.setStyleSheet("""
            background-color: #555555; 
            color: white; 
            padding: 5px; 
            border-radius: 5px;
            font-family: 'Roboto', sans-serif;
            font-size: 14px;
        """)
        layout.addWidget(solve_button2)
        
        self.setLayout(layout)

    def set_cell_style(self, cell, row, col):
        block_color = "#333333" if (row // 3 + col // 3) % 2 == 0 else "#444444"
        cell.setStyleSheet(f"""
            background-color: {block_color}; 
            color: white; 
            border: 1px solid white;
            border-radius: 5px;
            font-family: 'Roboto', sans-serif;
            font-size: 18px;
        """)

    def update_board(self, row, col, text):
        value = int(text) if text else None
        self.board.set_value(row, col, value)

    def apply_input_to_board(self):
        input_text = self.input_field.text()
        if len(input_text) != 81 or not input_text.isdigit():
            print("Please enter exactly 81 digits (0 for empty cells).")
            return

        for i in range(81):
            row = i // 9
            col = i % 9
            value = int(input_text[i])
            self.board.set_value(row, col, value if value != 0 else None)
            self.cells[(row, col)].setText(str(value) if value != 0 else '')

            if value != 0:
                self.cells[(row, col)].setReadOnly(True)
                self.cells[(row, col)].setStyleSheet(
                    self.cells[(row, col)].styleSheet() + "background-color: #222222; font-weight: bold;"
                )

        self.input_field.clear()

    def solve_sudoku(self):
        solver = Algorithm1Solver(self.board, self.cells)
        solved, solve_time = solver.solve()
        if solved:
            print(f"Sudoku solved in {solve_time:.4f} seconds")
        else:
            print("No solution found.")
            
    def solve_sudoku2(self):
        solver = Algorithm2Solver(self.board, self.cells)
        solved, solve_time = solver.solve()
        if solved:
            print(f"Sudoku solved in {solve_time:.4f} seconds")
        else:
            print("No solution found.")
    

app = QApplication(sys.argv)
window = SudokuSolverApp()
window.show()
sys.exit(app.exec_())
