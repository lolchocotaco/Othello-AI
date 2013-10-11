import pygame, sys, time, copy
from pygame.locals import *

from classes import Board
from const import *

# Other constants
GREEN = ( 75,166, 50)
BLUE = (50,75,166)
FPS = 10 # frames per second to update the screen
WINDOWWIDTH = 640 # width of the program's window, in pixels
WINDOWHEIGHT = 480 # height in pixels
SPACESIZE = 50 # width & height of each space on the board, in pixels
BOARDWIDTH = 8 # how many columns of spaces on the game board
BOARDHEIGHT = 8 # how many rows of spaces on the game board
WHITE_TILE = 'WHITE_TILE' # an arbitrary but unique value
BLACK_TILE = 'BLACK_TILE' # an arbitrary but unique value
EMPTY_SPACE = 'EMPTY_SPACE' # an arbitrary but unique value
HINT_TILE = 'HINT_TILE' # an arbitrary but unique value
ANIMATIONSPEED = 25 # integer from 1 to 100, higher is faster animation
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * SPACESIZE)) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * SPACESIZE)) / 2)



def testGame():
    b = Board()
    print b.board
    global MAINCLOCK, DISPLAYSURF
    pygame.init()
    MAINCLOCK = pygame.time.Clock()


    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT),0,32)
    DISPLAYSURF.fill(BLUE)

    mousex = 0
    mousey = 0
    pygame.display.set_caption('Chocotaco Othello')

    # pygame.draw.circle(DISPLAYSURF, (0, 0 , 0), (300, 50), 20, 0)
    pygame.draw.rect(DISPLAYSURF,GREEN,(XMARGIN,YMARGIN,WINDOWWIDTH-2*XMARGIN,WINDOWHEIGHT-2*YMARGIN))



    while True: # Game Loop
        for event in pygame.event.get():
            if event.type ==QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


if __name__ == "__main__" :
    testGame()

