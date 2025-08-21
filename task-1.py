def solveSudoku(board):
    def is_valid(board, row, col, num):
       
        for i in range(9):
            if board[row][i] == num:
                return False

        
        for i in range(9):
            if board[i][col] == num:
                return False

        
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == num:
                    return False

        return True

    def backtrack(board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == ".":  
                    for num in map(str, range(1, 10)):
                        if is_valid(board, i, j, num):
                            board[i][j] = num
                            if backtrack(board):  
                                return True
                            board[i][j] = "." 
                    return False
        return True

    backtrack(board)



sudoku_board = [
   ["5","3",".",".","7",".",".",".","."],
   ["6",".",".","1","9","5",".",".","."],
   [".","9","8",".",".",".",".","6","."],

   ["8",".",".",".","6",".",".",".","3"],
["4",".",".","8",".","3",".",".","1"],
["7",".",".",".","2",".",".",".","6"],

[".","6",".",".",".",".","2","8","."],
[".",".",".","4","1","9",".",".","5"],
[".",".",".",".","8",".",".","7","9"]
]

solveSudoku(sudoku_board)

for row in sudoku_board:
    print(row)
