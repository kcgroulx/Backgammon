from enum import Enum
import random

NUM_OF_SPACES = 26

PLAYER_WHITE = "WHITE"
PLAYER_BLACK = "BLACK"
PLAYER_EMPTY = "EMPTY"

#Game states
STATE_INIT = 0
STATE_ROLL = 1
STATE_MOVE = 2

class Space:
    def __init__(self, color, numOfPieces:int):
        self.color:str = color
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
        self.boardData = [Space(PLAYER_EMPTY, 0) for _ in range(NUM_OF_SPACES)]
        self.gameState = STATE_INIT
        self.playerTurn = PLAYER_WHITE
        self.dice = []
        self.legalMoves:list[int] = []
        self.selectedSpace = -1
        self.barBlack = 0
        self.barWhite = 0
        self.whiteHome = 0
        self.blackHome = 0
    
    def SetBoard(self):
        self.boardData[1] = Space(PLAYER_WHITE, 2)
        self.boardData[12] = Space(PLAYER_WHITE, 5)
        self.boardData[17] = Space(PLAYER_WHITE, 3)
        self.boardData[19] = Space(PLAYER_WHITE, 5)
        self.boardData[24] = Space(PLAYER_BLACK, 2)
        self.boardData[13] = Space(PLAYER_BLACK, 5)
        self.boardData[8] = Space(PLAYER_BLACK, 3)
        self.boardData[6] = Space(PLAYER_BLACK, 5)
    
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
    
    def MakeMove(self, index:int):
        if index > len(self.legalMoves):
            raise ValueError("Invalid legal move index")

        selectedSpace = self.boardData[self.selectedSpace]
        indexToMoveTo = self.legalMoves[index]
        spaceToMoveTo = self.boardData[indexToMoveTo]
        
        #Remove piece from selected space
        selectedSpace.RemovePiece()

        #Add piece to selected square
        if spaceToMoveTo.color == PLAYER_EMPTY:
            spaceToMoveTo.color = selectedSpace.color
            spaceToMoveTo.numOfPieces += 1
        elif spaceToMoveTo.color == selectedSpace.color:
            spaceToMoveTo.numOfPieces += 1
        elif spaceToMoveTo.color != selectedSpace.color: # Hit
            if spaceToMoveTo.color == PLAYER_WHITE:
                self.boardData[0].numOfPieces += 1
            elif spaceToMoveTo.color == PLAYER_BLACK:
                self.boardData[25].numOfPieces += 1
            spaceToMoveTo.RemovePiece()


        self.dice.pop(index)
        if len(self.dice) == 0:
            self.NextTurn()

        
