import pygame, sys, time, copy,numpy
from pygame.locals import *

from classes import *
from const import *

def playGame():
    while True: # Game Loop
        player = raw_input("Black or white? (b/w")
        move = raw_input("Input new move")




def testGame():
    b = Board()
    g = GUI()
    g.updateBoard(b.board)
    # playGame()
    while True:
        gridXY = g.getClick()
        b.putTile(gridXY,BLK)
        g.updateBoard(b.board)

if __name__ == "__main__" :
    testGame()
    # drawBoard()

