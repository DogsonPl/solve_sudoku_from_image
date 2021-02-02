import sys
import pytesseract
from cv2 import cv2
import numpy as np
import threading
import copy
import webbrowser
import time


class ReadSudokuBoard:
    def __init__(self, path_to_file):
        print("""Note: if image is bad quality or is small size, program can read wrong numbers 
On image should be only sudoku without background""")
        self.reading = True
        self.progress = 0
        threading._start_new_thread(self.reading_photo_progress_bar, ())

        pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

        self.sudoku_board = np.zeros((9, 9), dtype=np.uint8)
        try:
            self.sudoku_board_image = cv2.imread(path_to_file)
            self.resized_sudoku_board_image = cv2.resize(self.sudoku_board_image, (900, 900))
        except cv2.error:
            print(f"I can't find file in {path_to_file}")
            input("Click enter to close program")
            sys.exit()

    def reading_photo_progress_bar(self):
        while self.reading:
            print(f"Reading image...{self.progress}%", end="\r")
            time.sleep(0.1)
        print("\n")

    def get_data_from_image(self):
        x = 0
        to_count_progress = 100/81
        for i in range(9):
            try:
                for ii in range(9):
                    x += 1
                    self.progress = int(to_count_progress*x)
                    num = pytesseract.image_to_string(self.resized_sudoku_board_image[10 + i*100:(i+1)*100 - 10, 10 + ii*100:(ii+1)*100 - 10],
                                                      config="--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789")
                    if num:
                        try:
                            self.sudoku_board[i][ii] = num
                        except ValueError:
                            pass
            except pytesseract.pytesseract.TesseractNotFoundError:
                self.reading = False
                time.sleep(0.15)
                link_to_download = "https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20201127.exe"
                open_web_browser = input(f"You have to install {link_to_download}\nWrite 1 to open download link or click enter to close program")
                if open_web_browser == "1":
                    webbrowser.open(link_to_download)
                sys.exit()

        self.reading = False
        self.confirm_sudoku_board()
        return self.sudoku_board

    def confirm_sudoku_board(self):
        time.sleep(0.15)
        print(f"Sudoku board:\n{self.sudoku_board}")
        while True:
            confirm = input("Write '1' if program good loaded sudoku board or '0' if you want make fix: ")
            if confirm == "1":
                break
            elif confirm == "0":
                self.manual_sudoku_board_fix()
                break

    def manual_sudoku_board_fix(self):
        row = get_int_from_user("Write in which row you want make change (from 1 to 9) or 'q' to get back: ", 9)
        if row is None:
            self.confirm_sudoku_board()
        else:
            nums_in_row = []
            for i in self.sudoku_board[:][row-1]:
                nums_in_row.append(i)
            print(f"Numbers in {row-1} row:\n{nums_in_row}")
            column = get_int_from_user("Write in which column you want change number (from 1 to 9) or 'q' to get back: ", 9)
            if column is None:
                self.confirm_sudoku_board()
            else:
                new_number = get_int_from_user("Write to which number you want to cahge this number (from 1 to 9) or 'q' to get back: ", 9)
            if column is None:
                pass
            else:
                self.sudoku_board[row-1][column-1] = new_number
            self.confirm_sudoku_board()


def get_int_from_user(text, max):
    while True:
        try:
            num = input(text)
            num = int(num)
        except ValueError:
            if num == "q":
                break
            else:
                continue
        if num > max or num < 1:
            continue
        else:
            return num


# tbh algorithm to solve sudoku isn't mine, I,m not the best in math :(
class SudokuSolver:
    def __init__(self, sudoku_board):
        self.sudoku_board = sudoku_board

    def find_next_empty(self):
        for r in range(9):
            for c in range(9):
                if self.sudoku_board[r][c] == 0:
                    return r, c
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

        for r in range(row_start, row_start + 3):
            for c in range(col_start, col_start + 3):
                if self.sudoku_board[r][c] == guess:
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


def write_solution_on_photo(path_to_file, old_board, solved_board):
    image = cv2.imread(path_to_file)
    image = cv2.resize(image, (900, 900))
    x_place = 10
    y_place = 90
    for i in range(9):
        for ii in range(9):
            if old_board[i][ii] != solved_board[i][ii]:
                image = cv2.putText(image, text=str(solved_board[i][ii]), org=(x_place, y_place), fontFace=cv2.FONT_ITALIC,
                                    fontScale=3, color=(0, 200, 0), thickness=4)
            x_place += 100
        x_place = 10
        y_place += 100
    cv2.imwrite(f"solved-{path_to_file}", image)


if __name__ == '__main__':
    path_to_file = input("Give path to your sudoku image: ")
    sudoku_board = ReadSudokuBoard(path_to_file).get_data_from_image()
    old_board = copy.deepcopy(sudoku_board)
    solve = SudokuSolver(sudoku_board).solve_sudoku()
    if not solve:
        print("Can`t solve sudoku :( Click enter to continue")
        input()
        sys.exit()
    write_solution_on_photo(path_to_file, old_board, sudoku_board)
