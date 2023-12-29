
NUM_OF_SPACES = 24

PLAYER_WHITE = 0
PLAYER_BLACK = 1
PLAYER_EMPTY = 255

class Space:
    def __init__(self, color:int, numOfPieces:int):
        self.color = color
        self.numOfPieces = numOfPieces

class Board:    
    def __init__(self):
        self.boardData = [Space(PLAYER_EMPTY,0) for _ in range(NUM_OF_SPACES)]

    
