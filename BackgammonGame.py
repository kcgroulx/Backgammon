import pygame
import Pygammon as pg
import sys

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255,0,0)
YELLOW = (255,255,0)
BOARD_COLOR = (3, 52, 133)

#Bar
BAR_WIDTH = 100

#Display
WIDTH, HEIGHT = 14 * BAR_WIDTH, 800

#Triangle
TRIANGLE_WIDTH = 35
TRIANGLE_HEIGHT = 380
QUADRENT_WIDTH = (WIDTH - BAR_WIDTH)/2

#Pieces
PIECE_SIZE = 35
PIECE_SPACING = 5
PIECE_COLOR_BLACK = (20, 20, 50)
PIECE_COLOR_WHITE = (220, 220, 220)

#Roll Dice Button
ROLL_DICE_BUTTON_WIDTH = int(BAR_WIDTH)
rollDiceButton = pygame.Rect(7*BAR_WIDTH, HEIGHT-100, ROLL_DICE_BUTTON_WIDTH, 50)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Backgammon')

def SpaceToPixel(space:int):
    if space >= 1 and space < 7:
        return (BAR_WIDTH*(0.5 + space), 0)
    elif space < 13:
        return (BAR_WIDTH*(1.5 + space), 0)
    elif space < 19:
        return (BAR_WIDTH*(26.5 - space), HEIGHT)
    elif space < 25:
        return (BAR_WIDTH*(25.5 - space), HEIGHT)
    else:
        raise ValueError("Invalid space value")

def DrawTriangles():
    for i in range(1, 25):
        x,y = SpaceToPixel(i)
        vertices = [(x-TRIANGLE_WIDTH, y),(x+TRIANGLE_WIDTH, y), (x, TRIANGLE_HEIGHT if i < 13 else HEIGHT-TRIANGLE_HEIGHT)]
        color = WHITE if i % 2 == 0 else BLACK
        pygame.draw.polygon(screen, color, vertices)

def DrawPieces(board:pg.Board):
    for i in range(pg.NUM_OF_SPACES):
        space = board.boardData[i]
        if i != 0 and i != 25:
            x,y = SpaceToPixel(i)
            if(space.color != pg.PLAYER_EMPTY):
                for j in range(space.numOfPieces):
                    if i < 13:
                        pos = (x, y + j*( 2 * PIECE_SIZE + PIECE_SPACING) + PIECE_SIZE)
                    else:
                        pos = (x, y - j*( 2 * PIECE_SIZE + PIECE_SPACING) - PIECE_SIZE)
                    color = PIECE_COLOR_WHITE if space.color == pg.PLAYER_WHITE else PIECE_COLOR_BLACK
                    pygame.draw.circle(screen, color, pos, PIECE_SIZE)

        if i in board.legalMoves:
            if i < 13:
                pos = (x, y + space.numOfPieces*( 2 * PIECE_SIZE + PIECE_SPACING) + PIECE_SIZE)
            else:
                pos = (x, y - space.numOfPieces*( 2 * PIECE_SIZE + PIECE_SPACING) - PIECE_SIZE)
            pygame.draw.circle(screen, YELLOW, pos, PIECE_SIZE)  

def DrawBar():
    square_rect = pygame.Rect(7 * BAR_WIDTH, 0, BAR_WIDTH, HEIGHT)
    pygame.draw.rect(screen, BLACK, square_rect)

def DrawHomes():
    square_rect = pygame.Rect(0, 0, BAR_WIDTH, HEIGHT)
    pygame.draw.rect(screen, BLACK, square_rect)

def DrawBoard(board:pg.Board):
    screen.fill(BOARD_COLOR)
    DrawTriangles()
    DrawBar()
    DrawHomes()
    DrawPieces(board)
    DrawRollDiceButton()
    pygame.display.flip()

def DrawRollDiceButton():
    pygame.draw.rect(screen, RED, rollDiceButton)

def IsButtonPressed(pos, button):
    x, y = pos
    return button.left <= x <= button.right and button.top <= y <= button.bottom

def PixelToSpace(pos):
    x, y = pos
    if y < HEIGHT / 2:
        if x > 0 and x < BAR_WIDTH * 7:
            return int(x/BAR_WIDTH)
        elif x > BAR_WIDTH * 8 and x < WIDTH: 
            return int((x/BAR_WIDTH) - 1)
    elif y > HEIGHT / 2:
        if x < WIDTH and x > BAR_WIDTH * 8: 
            return int(27 - (x/BAR_WIDTH))
        elif x < BAR_WIDTH * 7 and x > 0:
            return int(26 - (x/BAR_WIDTH))
    return -1

def main():
    clock = pygame.time.Clock()
    running = True
    board = pg.Board()
    board.SetBoard()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if IsButtonPressed(pygame.mouse.get_pos(), rollDiceButton):
                   board.RollDice()
                   print(board.dice)
                
                spacePressed = PixelToSpace(pygame.mouse.get_pos())
                if spacePressed != -1:
                    if spacePressed in board.legalMoves:
                        index = board.legalMoves.index(spacePressed)
                        board.MakeMove(index)
                    else:
                        board.SelectSpace(spacePressed)
                
        DrawBoard(board)
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
