from cv2 import cv2
import os


# backtracking algorithm
class SudokuSolver:
    def __init__(self, sudoku_board):
        self.sudoku_board = sudoku_board

    def find_next_empty(self):
        for row in range(9):
            for col in range(9):
                if self.sudoku_board[row][col] == 0:
                    return row, col
        return None, None

    def is_valid(self, guess, row, col):
        row_vals = self.sudoku_board[row]
        if guess in row_vals:
            return False
        col_vals = [self.sudoku_board[i][col] for i in range(9)]
        if guess in col_vals:
            return False

        row_start = (row // 3) * 3
        col_start = (col // 3) * 3

        for row in range(row_start, row_start + 3):
            for column in range(col_start, col_start + 3):
                if self.sudoku_board[row][column] == guess:
                    return False
        return True

    def solve_sudoku(self):
        row, col = self.find_next_empty()
        if row is None:
            return True
        for guess in range(1, 10):
            if self.is_valid(guess, row, col):
                self.sudoku_board[row][col] = guess
                if self.solve_sudoku():
                    return True
            self.sudoku_board[row][col] = 0
        return False


class SaveSolvedSudoku:
    def __init__(self, path_to_file, old_board, solved_board):
        self.path_to_file = path_to_file
        self.solved_board = solved_board
        self.old_board = old_board

    def write_solution_on_photo(self, ):
        image = cv2.imread(self.path_to_file)
        image = cv2.resize(image, (900, 900))
        x_place = 10
        y_place = 90
        for i in range(9):
            for j in range(9):
                if self.old_board[i][j] != self.solved_board[i][j]:
                    image = cv2.putText(image, text=str(self.solved_board[i][j]), org=(x_place, y_place),
                                        fontFace=cv2.FONT_ITALIC, fontScale=3, color=(0, 200, 0), thickness=4)
                x_place += 100
            x_place = 10
            y_place += 100
        self.save_file(image)

    def save_file(self, image):
        filename = os.path.splitext(self.path_to_file)[0]
        extension = os.path.splitext(self.path_to_file)[1]
        path_to_save_file = f"{filename}-solved{extension}"
        cv2.imwrite(path_to_save_file, image)
        os.startfile(path_to_save_file)
