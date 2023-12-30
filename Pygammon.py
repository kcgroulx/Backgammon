from enum import Enum
import random



NUM_OF_SPACES = 24

PLAYER_WHITE = 0
PLAYER_BLACK = 1
PLAYER_EMPTY = 255

#Game states
STATE_INIT = 0
STATE_ROLL = 1
STATE_MOVE = 2

class Space:
    def __init__(self, color:int, numOfPieces:int):
        self.color = color
        self.numOfPieces = numOfPieces
    
    def RemovePiece(self):
        self.numOfPieces -= 1
        if self.numOfPieces < 1:
            self.color = PLAYER_EMPTY
    
    def AddPiece(self, color):
        if self.color == color or self.color == PLAYER_EMPTY:
            self.numOfPieces += 1
        else:
            self.numOfPieces = 1
        self.color = color

class Board:
    def __init__(self):
        self.boardData = [Space(PLAYER_EMPTY,0) for _ in range(NUM_OF_SPACES)]
        self.gameState = STATE_INIT
        self.playerTurn = PLAYER_WHITE
        self.dice = []
        self.legalMoves = []
        self.selectedSpace = -1
        self.barBlack = 0
        self.barWhite = 0
    
    def SetBoard(self):
        self.boardData[0] = Space(PLAYER_WHITE, 2)
        self.boardData[11] = Space(PLAYER_WHITE, 5)
        self.boardData[16] = Space(PLAYER_WHITE, 3)
        self.boardData[18] = Space(PLAYER_WHITE, 5)
        self.boardData[23] = Space(PLAYER_BLACK, 2)
        self.boardData[12] = Space(PLAYER_BLACK, 5)
        self.boardData[7] = Space(PLAYER_BLACK, 3)
        self.boardData[5] = Space(PLAYER_BLACK, 5)

    def MovePiece(self, index):
        self.boardData[index].AddPiece(self.playerTurn)
        

    def NextTurn(self):
        self.playerTurn = PLAYER_WHITE if self.playerTurn == PLAYER_BLACK else PLAYER_BLACK

    def RollDice(self):
        die1 = random.randint(1,6)
        die2 = random.randint(1,6)
        if die1 == die2:
            self.dice = [die1 for _ in range(4)]
        else:
            self.dice = [die1, die2]
        self.dice.sort()

    def GenerateLegalMoves(self, index:int):
        space = self.boardData[index]
        legalMoves = []
        if space.color == self.playerTurn:
            moveSet = set(self.dice)
            for move in moveSet:
                target = self.boardData[index + move] if self.playerTurn == PLAYER_WHITE else self.boardData[index - move]

                if target.color == self.playerTurn or target.color == PLAYER_EMPTY or (target.numOfPieces == 1 and target.color != self.playerTurn):
                    if self.playerTurn == PLAYER_WHITE:
                        legalMoves.append(index + move)
                    elif self.playerTurn == PLAYER_BLACK:
                        legalMoves.append(index - move)
        return legalMoves

    def SelectSpace(self, index:int):
        self.legalMoves = self.GenerateLegalMoves(index)
        self.selectedSpace = index
    
    def MakeMove(self, index):
        if index > len(self.legalMoves):
            raise ValueError("Invalid legal move index")
        
        self.boardData[self.selectedSpace].RemovePiece()
        self.MovePiece(self.legalMoves[index])

        self.dice.pop(index)
        if len(self.dice) == 0:
            self.NextTurn()
            print(self.playerTurn)

        
