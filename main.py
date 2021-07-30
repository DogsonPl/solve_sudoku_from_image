import copy

import easygui

import read_sudoku_board
import solve_sudoku


def get_sudoku_boards():
    sudoku_board = read_sudoku_board.ReadSudokuBoardImage(PATH_TO_SUDOKU_BOARD).get_data_from_image()
    sudoku_board = read_sudoku_board.ManualSudokuBoardFix(sudoku_board).confirm_sudoku_board()
    old_board = copy.deepcopy(sudoku_board)
    return sudoku_board, old_board


def solve_sudoku_board():
    solved = solve_sudoku.SudokuSolver(SUDOKU_BOARD).solve_sudoku()
    if not solved:
        print("Can`t solve sudoku :( \nClick enter to continue")
        input()
    else:
        solve_sudoku.SaveSolvedSudoku(PATH_TO_SUDOKU_BOARD, OLD_BOARD, SUDOKU_BOARD).write_solution_on_photo()


if __name__ == '__main__':
    PATH_TO_SUDOKU_BOARD = easygui.fileopenbox("Choose image with sudoku board")
    SUDOKU_BOARD, OLD_BOARD = get_sudoku_boards()
    solve_sudoku_board()
