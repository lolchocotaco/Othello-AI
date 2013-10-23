# Class for board

from const import *
import pygame,sys
from pygame.locals import *
from board import Board
from gui import GUI

class Othello:
    def __init__(self):
        self.g = GUI()
        self.b = Board()
        self.showMenu()

    def showMenu(self):
        # input =
        self.player1, self.player2, noHumans = self.g.getPlayer()
        if noHumans:
            print("The computers will battle")

        print("LET THE GAMES BEGIN!")
        self.g.showBoard()

    def play(self):
        while True:
        # Get valid black moves
            validMoves = self.b.getValidMoves(self.player1)
            self.g.updateBoard(self.b, self.player1)
            # If there are any valid moves get Clicks
            if validMoves:
                gridXY = self.g.getClick()
                # print(gridXY)
                # If the click is in the valid --> Put tile, and let computer make moves
                if gridXY in validMoves:
                    self.b.putTile(gridXY, self.player1)
                    self.g.updateBoard(self.b)
                    pygame.time.wait(500)
                    self.b.makeCompMove(self.player2)
                    self.g.updateBoard(self.b)
            else:
                print("No valid Moves.. you skipped")
                self.b.makeCompMove(self.player2)
                self.g.updateBoard(self.b, self.player2)

            # TODO Fix Game flow
            # Made player class.. Black always goes first


            # Check end state
            if self.b.checkEnd():
                    print("Game ended")
                    tileCount = self.b.getTileCount()
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







