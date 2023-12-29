import pygame
import Pygammon as pg
import sys

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255,0,0)

BOARD_COLOR = (3, 52, 133)

# Set up the display
WIDTH, HEIGHT = 1300, 800

BAR_WIDTH = 100

TRIANGLE_WIDTH = 35
TRIANGLE_HEIGHT = 380

PIECE_SIZE = 35
PIECE_SPACING = 5
PIECE_COLOR_BLACK = (20, 20, 50)
PIECE_COLOR_WHITE = (220, 220, 220)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Backgammon')

def SpaceToPixel(space:int):
    x,y = 0,0
    quad_width = (WIDTH - BAR_WIDTH) / 2
    space_size = quad_width / 7
    if space < 6 and space >= 0:
        return (space_size*(space+1), 0)
    elif space < 12:
        return (quad_width+BAR_WIDTH + space_size*(space-5), 0)
    elif space < 18:
        return (quad_width+BAR_WIDTH + space_size*(18-space), HEIGHT)
    elif space < 24:
        return (space_size*(24-space), HEIGHT)
    else:
        raise ValueError("Invalid space value")

def DrawTriangles():
    for i in range(24):
        x,y = SpaceToPixel(i)
        vertices = [(x - TRIANGLE_WIDTH, y),(x + TRIANGLE_WIDTH, y), (x, TRIANGLE_HEIGHT if i < 12 else HEIGHT-TRIANGLE_HEIGHT)]
        color = WHITE if i % 2 == 0 else BLACK
        pygame.draw.polygon(screen, color, vertices)


def DrawPieces(board:pg.Board):
    for i in range(pg.NUM_OF_SPACES):
        space = board.boardData[i]
        if(space.color != pg.PLAYER_EMPTY):
            x,y = SpaceToPixel(i)
            for j in range(space.numOfPieces):
                pos = (x, y + j*( 2 * PIECE_SIZE + PIECE_SPACING))
                color = PIECE_COLOR_WHITE if space.color == pg.PLAYER_WHITE else PIECE_COLOR_BLACK
                pygame.draw.circle(screen, color, pos, PIECE_SIZE )
        

def DrawBar():
    square_rect = pygame.Rect((WIDTH-BAR_WIDTH)/2, 0, BAR_WIDTH, HEIGHT)
    pygame.draw.rect(screen, BLACK, square_rect)

def DrawBoard(board:pg.Board):
    DrawTriangles()
    DrawBar()
    DrawPieces(board)

def main():
    clock = pygame.time.Clock()
    running = True

    board = pg.Board()
    board.boardData[0].color = pg.PLAYER_WHITE
    board.boardData[0].numOfPieces = 4

    board.boardData[2] = pg.Space(pg.PLAYER_BLACK,2)

    board.boardData[7].color = pg.PLAYER_BLACK
    board.boardData[7].numOfPieces = 3

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BOARD_COLOR)
        DrawBoard(board)

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
