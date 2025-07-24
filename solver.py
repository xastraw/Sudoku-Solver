from SudokuClass import Sudoku
from getBoard import scrapeBoard, fillBoard
import time
import copy

s = Sudoku()


def possibilities(board): #returns all posible values in a dict and returns squares with 1 possible value in a list
    
    zero_list = s.getBlanks(board)

    digits = '123456789'
    grid = {}
    
    for row, col in zero_list:
        digitSet = "" #will be the possible digits for each blank spot
        
        for digit in digits:
            if s.validMove(board, row, col, int(digit)) == True:
                digitSet +=  digit
        grid.update({(row, col) : digitSet})

    sortedGrid = dict(sorted(grid.items(), key=lambda item: len(item[1]))) #sorts the squares from lowest num of possibilites to highest num

    return sortedGrid
    

def backtrack(board):
    #make using a dfs starting with the squares that have the lowest number of possiblities 
    board=copy.deepcopy(board)

    #Contraint propagation on all squares with single possibilities
    while True:
        grid = possibilities(board)
        singles = [(pos, vals) for pos, vals in grid.items() if len(vals) == 1]
        if not singles:
            break
        for (row, col), val in singles:
            board[row][col] = int(val)
    
    #Check for solution
    if s.validSolution(board):
        return board
   
    #check for any contradiction
    grid = possibilities(board)
    if any(len(vals) == 0 for vals in grid.values()) or len(grid) == 0:
        return "unsolvable"
    

    (row, col), vals = next(iter(grid.items())) #pick the box with the minimum remaining values
    for number in vals:
        boardCopy = copy.deepcopy(board)
        boardCopy[row][col] = int(number)
        result = backtrack(boardCopy)
        if result != "unsolvable":
            return result
    return "unsolvable"



def main():    
    #testing boards
    mediumBoard = [
        [0, 6, 0, 0, 0, 0, 0, 0, 0],
        [5, 0, 4, 0, 8, 0, 0, 0, 3],
        [0, 0, 1, 0, 0, 0, 0, 6, 0],
        [0, 7, 0, 0, 0, 0, 0, 0, 8],
        [2, 0, 0, 0, 9, 6, 1, 4, 0],
        [0, 0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 4, 6, 0, 0, 9, 0],
        [0, 0, 0, 0, 5, 1, 7, 2, 0],
        [3, 0, 0, 0, 0, 9, 0, 0, 0]]
    mediumBoard_solved = [
        [9, 6, 7, 1, 3, 5, 4, 8, 2],
        [5, 2, 4, 6, 8, 7, 9, 1, 3],
        [8, 3, 1, 9, 4, 2, 5, 6, 7],
        [6, 7, 9, 5, 1, 4, 2, 3, 8],
        [2, 8, 3, 7, 9, 6, 1, 4, 5],
        [1, 4, 5, 8, 2, 3, 6, 7, 9],
        [7, 5, 2, 4, 6, 8, 3, 9, 1],
        [4, 9, 8, 3, 5, 1, 7, 2, 6],
        [3, 1, 6, 2, 7, 9, 8, 5, 4]]
    easyBoard = [
        [6, 0, 5, 0, 0, 7, 2, 3, 4],
        [2, 1, 3, 5, 0, 6, 0, 0, 0],
        [0, 4, 0, 0, 0, 9, 6, 0, 0],
        [0, 3, 1, 4, 0, 0, 0, 0, 8],
        [0, 5, 0, 6, 7, 3, 0, 0, 0],
        [7, 0, 0, 0, 1, 0, 0, 4, 5],
        [5, 6, 2, 0, 0, 0, 4, 0, 0],
        [0, 0, 0, 8, 3, 0, 0, 2, 0],
        [3, 0, 0, 2, 6, 5, 0, 7, 0]]
    easyBoard_solved = [
        [6, 9, 5, 1, 8, 7, 2, 3, 4],
        [2, 1, 3, 5, 4, 6, 8, 9, 7],
        [8, 4, 7, 3, 2, 9, 6, 5, 1],
        [9, 3, 1, 4, 5, 2, 7, 6, 8],
        [4, 5, 8, 6, 7, 3, 9, 1, 2],
        [7, 2, 6, 9, 1, 8, 3, 4, 5],
        [5, 6, 2, 7, 9, 1, 4, 8, 3],
        [1, 7, 9, 8, 3, 4, 5, 2, 6],
        [3, 8, 4, 2, 6, 5, 1, 7, 9]]
    unsolvableBoard = [ #0,0 has no possible spots
        [0, 1, 2, 3, 4, 5, 6, 7, 8],  # Row uses 1–8 already, so 9 is the only missing number
        [9, 0, 0, 0, 0, 0, 0, 0, 0],  # Column 0 uses 9
        [3, 0, 0, 0, 0, 0, 0, 0, 0],  # Box (0,0) now has 3, 9
        [4, 0, 0, 0, 0, 0, 0, 0, 0],  # Column 0 now has 0, 3, 4, 9
        [5, 0, 0, 0, 0, 0, 0, 0, 0],  # ...
        [6, 0, 0, 0, 0, 0, 0, 0, 0],
        [7, 0, 0, 0, 0, 0, 0, 0, 0],
        [8, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0, 0, 0, 0]]
    hardBoard = [
        [0, 0, 0, 0, 0, 4, 1, 0, 0],
        [0, 4, 0, 9, 0, 0, 0, 6, 0],
        [1, 0, 0, 3, 8, 0, 0, 5, 0],
        [0, 0, 6, 0, 0, 0, 0, 0, 2],
        [0, 0, 0, 1, 0, 3, 0, 4, 5],
        [0, 0, 0, 0, 0, 0, 0, 9, 0],
        [0, 0, 8, 0, 0, 7, 0, 0, 0],
        [2, 0, 0, 0, 9, 0, 7, 0, 0],
        [6, 0, 0, 0, 5, 0, 0, 0, 4]]
    hardBoard_solved = [
        [8, 2, 5, 7, 6, 4, 1, 3, 9],
        [7, 4, 3, 9, 1, 5, 2, 6, 8],
        [1, 6, 9, 3, 8, 2, 4, 5, 7],
        [3, 1, 6, 5, 4, 9, 8, 7, 2],
        [9, 8, 2, 1, 7, 3, 6, 4, 5],
        [5, 7, 4, 6, 2, 8, 3, 9, 1],
        [4, 9, 8, 2, 3, 7, 5, 1, 6],
        [2, 5, 1, 4, 9, 6, 7, 8, 3],
        [6, 3, 7, 8, 5, 1, 9, 2, 4]]
    insaneBoard = [
        [0, 0, 2, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 9, 0, 7, 0, 0, 0],
        [0, 0, 9, 0, 0, 8, 0, 4, 1],
        [0, 5, 0, 0, 0, 6, 0, 0, 2],
        [0, 0, 0, 4, 0, 0, 7, 0, 0],
        [2, 0, 0, 0, 5, 0, 0, 8, 0],
        [0, 0, 6, 7, 8, 0, 3, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0],
        [4, 3, 0, 0, 6, 0, 0, 0, 0]]
    insaneBoard_solved = [
        [1, 8, 2, 6, 4, 5, 9, 3, 7],
        [5, 4, 3, 9, 1, 7, 2, 6, 8],
        [7, 6, 9, 2, 3, 8, 5, 4, 1],
        [3, 5, 1, 8, 7, 6, 4, 9, 2],
        [6, 9, 8, 4, 2, 3, 7, 1, 5],
        [2, 7, 4, 1, 5, 9, 6, 8, 3],
        [9, 1, 6, 7, 8, 2, 3, 5, 4],
        [8, 2, 5, 3, 9, 4, 1, 7, 6],
        [4, 3, 7, 5, 6, 1, 8, 2, 9]]

    testing = False
    autoFill = True


    if testing ==  False:
        board, chromeDriver = scrapeBoard("hard")
        

        s.print_board(board)
        startTime = time.time()
        returnBoard = backtrack(board)
        endTime = time.time()

        print(f"Time taken: {round(endTime-startTime, 3)} seconds")
        if returnBoard != "unsolvable":
            print("Board solved!")
            s.print_board(returnBoard)

        if autoFill == True:
            fillBoard(returnBoard, chromeDriver)
        else:
            chromeDriver.quit()

    else:
        board = insaneBoard
        solvedBoard = insaneBoard_solved


        s.print_board(board)
        startTime = time.time()
        returnBoard = backtrack(board)
        endTime = time.time()
        print(f"Time taken: {round(endTime-startTime, 3)} seconds")

        if returnBoard == solvedBoard:
            print("Board matches solved board")
        else:
            print("Board can't be solved")




main()