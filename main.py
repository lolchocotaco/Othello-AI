import pygame, sys, time, copy,numpy
from pygame.locals import *

from classes import *
from const import *


def playGame():
    while True: # Game Loop
        player = raw_input("Black or white? (b/w)")


def testGame():
    b = Board()
    g = GUI()
    g.updateBoard(b.board)
    # playGame()
    while True:
        validMoves = b.getValidMoves(BLK)
        print validMoves
        gridXY = g.getClick()
        if gridXY in validMoves:
            b.putTile(gridXY, BLK)
            g.updateBoard(b.board)

    #TODO apply checks before placing tile Call update board after moves (flips included)

if __name__ == "__main__" :
    testGame()
    # drawBoard()

