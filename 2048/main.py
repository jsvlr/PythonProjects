from random import randint
from os import system
from time import sleep

class myGame2048:
    # Give default size of the board (4x4)
    def __init__(self, row:int = 4, col:int = 4) -> None:
        self.row = row
        self.col = col
        self.score = 0
        self.board = []

    # This method will set the board by adding row and column with the vlaue of zero.
    def setBoard(self) -> None:
        # List comprehension to add 0 (zero) for each column in each row
        self.board = [[0 for _ in range(self.col)]for _ in range(self.row)]

        # Add 2 initial value for the board
        self.setTwo()
        self.setTwo()

    # This method will set the value for the board.
    def setTwo(self) -> None:
        
        # This condition will check if the board has available spot. If false then it will exit the method.
        if self.hasEmptyTile() == False:
            return
        
        # This loop will find a available spot
        while True:
            c = randint(0, self.col - 1)
            r = randint(0, self.row - 1)
            if self.board[r][c] == 0:
                self.board[r][c] = 2
                return 

    def getBoard(self) -> None:
        for row in self.board:
            row_board = " | ".join(f'{num:2}' for num in row)
            row_board = row_board.replace("0", " ")
            print(row_board)

    def slide(self, row:list) -> list:
        # This line will remove the zero on row
        filtered_row = [num for num in row if num != 0]
        # This loop will check if the next value of the current item inside the row is same
        for item in range(len(filtered_row) - 1):
            # If its the same it will times it self to two
            if filtered_row[item] == filtered_row[item + 1]:
                filtered_row[item] *= 2
                self.score += filtered_row[item]
                filtered_row[item + 1] = 0

        # This method will append 0 to the row to get back the zero 
        # [2, 0] -> [2, 0, 0, 0] 
        filtered_row = [num for num in filtered_row if num != 0]
        new_row = filtered_row + [0] * (self.row - len(filtered_row))
        return new_row 

    # This method will handle slide left.
    def slideLeft(self) -> None:
        # For each row on board will use slide method to move from current position to left.
        for r in range(self.row):
            self.board[r] = self.slide(self.board[r])
    
    # This method will handle slide right.
    def slideRight(self) -> None:
        # For each row on board will use the slide method to move from current position to right.
        for r in range(self.row):
             # The [::-1] means it will return a reverese row. 
             # [2,0,0,0] -> [0,0,0,2]
            row = self.slide(self.board[r][::-1])
            self.board[r] = row[::-1]

    # This method will handle slide up.
    def slideUp(self) -> None:
        for c in range(self.col):
            col = self.slide([self.board[r][c] for r in range(self.row)])
            for r in range(self.row):
                self.board[r][c] = col[r]

    # This method will handle slide down.
    def slideDown(self) -> None:
        for c in range(self.col):
            # the row will reversed first before using slide method
            col = self.slide([self.board[r][c] for r in range(self.row)][::-1])
            # this method will make the col back to its original position
            col = col[::-1]
            for r in range(self.row):
                self.board[r][c] = col[r]

    # This method will check each value inside the board if it has winning numbers.
    def checkWin(self) -> None:
        # This is the winning number
        winningNumbers = [2048, 4092, 8184]
        for r in range(self.row):
            for c in range(self.col):
                # This condition will chcek if the current value of tile is one of winning numbers
                if self.board[r][c] in winningNumbers:
                    print(f'Congratulation you got {self.board[r][c]}')
                    # i add return here to stop the loop when it hit the condition
                    return

    # This method will check if it has 0 in one of the tiles.
    def hasEmptyTile(self) -> bool:
        for r in self.board:
            if 0 in r:
                return True
        return False
    
    # This method will check if it has available move if not then it lose
    def hasLost(self) -> bool:
        for r in range(self.row):
            for c in range(self.col):
                # This will check if the board still have an available tile (0).
                if self.board[r][c] == 0:
                    return False
                # Get the current value of the tile.
                cur = self.board[r][c] 
                # This condition here check if the neighbor of the current tile has the same value of the current tile.
                if r > 0 and self.board[r - 1][c] == cur or r < self.row - 1 and self.board[r + 1][c] == cur or c > 0 and self.board[r][c - 1] == cur or c < self.col - 1 and self.board[r][c + 1] == cur:
                    return False
        return True

    # This method will handle all the moves.
    def handleSlide(self) -> None:
        # Get the move of the player.
        move:str = input('Your move: ').lower()

        # Store the method inside the dict
        keymove:dict = {
            'a':self.slideLeft,
            'd':self.slideRight,
            'w':self.slideUp,
            's':self.slideDown
        }

        # Check if the input is valid. If it is single char and it is valid key in the dict
        if len(move) == 1 and move in [k for k in keymove.keys()]:
            # Call the move inside the dict
            keymove[move]()
            # Add new value inside the board
            self.setTwo()
        else:
            # Print invalid if the move is more than 1 char or not valid key.
            print('Invalid!')
    
    # This method will start the game.
    def startGame(self):
        print('-------- Key Movements ----------')
        print('a. left\nw. up\ns. down\nd. right')
        
        # This loop while the hasLost method return False.
        while self.hasLost() is False:
            self.getBoard()
            self.checkWin()
            print('-' * 20)
            print(f'Score: {self.score}')
            self.handleSlide()
            sleep(0.25)
            system('cls')
        print('-------------------')
        self.getBoard()
        print('-------------------')
        print('Game Over!!')
        print(f'Final Score: {self.score}')


def main() -> None:
    game = myGame2048()
    game.setBoard()
    game.startGame()
   

if __name__ == "__main__":
    main()