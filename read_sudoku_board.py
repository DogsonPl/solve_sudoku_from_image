import webbrowser
import time
import numpy as np
import threading
import pytesseract
import sys
from cv2 import cv2


pytesseract.pytesseract.tesseract_cmd = "C://Program Files//Tesseract-OCR//tesseract.exe"


class ReadSudokuBoardImage:
    def __init__(self, path_to_file):
        print("""Note: if image is bad quality or is small size, program can read wrong numbers 
On image should be only sudoku without background""")
        self.reading_image = True
        self.progress = 0
        threading.Thread(target=self.loading_progress_bar, daemon=True).start()

        self.sudoku_board = np.zeros((9, 9), dtype=np.uint8)
        self.sudoku_board_image = cv2.imread(path_to_file)
        try:
            self.resized_sudoku_board_image = cv2.resize(self.sudoku_board_image, (900, 900))
        except cv2.error:
            input("Wrong file. Click enter to exit program")
            sys.exit()

    def loading_progress_bar(self):
        while self.reading_image:
            print(f"Reading image...{self.progress}%", end="\r")
            time.sleep(0.1)
        print("\n")

    def get_data_from_image(self):
        x = 0
        progress = 100/81
        for i in range(9):
            for j in range(9):
                x += 1
                self.progress = int(progress*x)
                try:
                    num = pytesseract.image_to_string(self.resized_sudoku_board_image[10+i*100:(i+1)*100-10, 10+j*100:(j+1)*100-10],
                                                      config="--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789")
                except pytesseract.pytesseract.TesseractNotFoundError:
                    self.on_tesseract_not_found_error()
                    break
                if num:
                    try:
                        self.sudoku_board[i][j] = num
                    except ValueError:
                        pass

        self.reading_image = False
        return self.sudoku_board

    def on_tesseract_not_found_error(self):
        self.reading_image = False
        time.sleep(0.15)
        link_to_download = "https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20201127.exe"
        open_web_browser = input(
            f"You have to install {link_to_download}\nWrite 1 to open download link or click enter to close program")
        if open_web_browser == "1":
            webbrowser.open(link_to_download)
        sys.exit()


class ManualSudokuBoardFix:
    def __init__(self, sudoku_board):
        self.sudoku_board = sudoku_board

    def confirm_sudoku_board(self):
        print(f"Sudoku board:\n{self.sudoku_board}")
        while True:
            confirm = input("Write '1' if program good loaded sudoku board or '0' if you want make fix: ")
            if confirm == "1":
                break
            elif confirm == "0":
                self.manual_sudoku_board_fix()
        return self.sudoku_board

    def manual_sudoku_board_fix(self):
        row = self.get_int_from_user("Write in which row you want make change (from 1 to 9) or 'q' to get back: ")
        if not row:
            return

        nums_in_row = []
        for i in self.sudoku_board[:][row-1]:
            nums_in_row.append(i)
        print(f"Numbers in {row-1} row:\n{nums_in_row}")

        column = self.get_int_from_user("Write in which column you want change number (from 1 to 9) or 'q' to get back: ")
        if not column:
            return

        new_number = self.get_int_from_user("Write to which number you want to cahge this number (from 1 to 9) or 'q' to get back: ")
        if not new_number:
            return

        self.sudoku_board[row-1][column-1] = new_number

    @staticmethod
    def get_int_from_user(text):
        while True:
            num = input(text)
            if num == "q":
                return False
            try:
                if 1 <= int(num) <= 9:
                    return num
            except ValueError:
                print("You have to give number between 0 and 9")
