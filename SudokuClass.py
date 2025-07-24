
class Sudoku:

    def print_board(self, board):
        for row in board:
            print(row)
        print("\n")
    
    def checkRow(self, board, row, value): #returns true if the input is not in the row
        return value not in board[row]
    
    def checkCol(self, board, col, value): #returns true if the input is not in the column
        return value not in [row[col] for row in board]

    def checkBox(self,  board, row, col, value): #returns true if the input num is not inside the box
        startRow = (row // 3)*3
        startCol = (col // 3) * 3

        box = [board[r][c] for r in range(startRow, startRow + 2)
                                for c in range(startCol, startCol + 2)]
        
        return value not in box
    
    def validMove(self, board, row, col, value): #returns true if an input is valid
        return (
            self.checkBox(board, row, col, value) and
            self.checkRow(board, row, value) and
            self.checkCol(board, col, value)
        )

    def getBlanks(self, b): #returns a set of the total number of blanks or 0s in the board
        blanks = set() #use a set because its quicker than a list
        for row_idx, row in enumerate(b):
            for col_idx, digit in enumerate(row):
                if digit == 0:
                    blanks.add((row_idx, col_idx))
                    #print(f"Zero found at row {row_idx}, column {col_idx}, total 0s: {len(blanks)}")
                    #blank positions will be row: blanks[-][0] and col: blanks[-][1]
        return blanks
    
    def validSolution(self, b):
        required = set(range(1, 10))
    
        #Check rows
        for row in b:
            if set(row) != required:
                return False

        #Check columns
        for col in range(9):
            if set(b[row][col] for row in range(9)) != required:
                return False
        
        #Check boxes
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                box = []
                for r in range(box_row, box_row + 3):
                    for c in range(box_col, box_col+3):
                        box.append(b[r][c])
                if set(box) != required:
                    return False
        return True