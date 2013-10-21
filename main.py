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

    # playGame()
    while True:
        # Get valid black moves
        validMoves = b.getValidMoves(BLK)
        g.updateBoard(b, BLK)
        # If there are any valid moves get Clicks
        if validMoves:
            gridXY = g.getClick()
            # print(gridXY)
            # If the click is in the valid --> Put tile, and let computer make moves
            if gridXY in validMoves:
                b.putTile(gridXY, BLK)
                g.updateBoard(b)
                pygame.time.wait(500)
                b.makeCompMove(WHT)
                g.updateBoard(b)
        else:
            print("No valid Moves.. you skipped")
            b.makeCompMove(WHT)
            g.updateBoard(b,WHT)

        # TODO Fix game flow. Possibly wrap game in another othello class


        # Check end state
        if b.checkEnd():
                print("Game ended")
                tileCount = b.getTileCount()
                print(tileCount)
                if tileCount[0] > tileCount[1]:
                    print("Black wins")
                elif tileCount[0]< tileCount[1]:
                    print("White wins")
                else:
                    print("Magically a draw")
                pygame.time.wait(5000)
                pygame.quit()
                sys.exit()

    #TODO apply checks before placing tile Call update board after moves (flips included)

if __name__ == "__main__" :
    testGame()


