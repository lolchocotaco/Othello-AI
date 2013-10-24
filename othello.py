# Class for board

from const import *
import pygame,sys
from pygame.locals import *
from board import Board
from gui import GUI
from players import *

class Othello:
    def __init__(self):
        self.g = GUI()
        self.b = Board()
        self.players =[None,None]
        self.showMenu()

    def showMenu(self):
        # input =
        players = self.g.getPlayer()
        if players[0] == "h":
            self.players[0] = humanPlayer(BLK,self.g)
            self.players[1] = compPlayer(WHT,self.g)
        elif players[1] == "h":
            self.players[0] = compPlayer(BLK,self.g)
            self.players[1] = humanPlayer(WHT,self.g)
        else:
            self.players[0] = compPlayer(BLK,self.g)
            self.players[1] = compPlayer(WHT,self.g)
        self.g.showBoard()
        print("LET THE GAMES BEGIN!")



    def play(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
        # Get valid black moves
            for player in self.players:
                validMoves = self.b.getValidMoves(player.color)  # Get list of valid moves
                if validMoves:
                    self.g.updateBoard(self.b, player.color) # Update board to show possible moves
                    pygame.time.wait(500)
                    gridXY = player.getMove(validMoves)
                    self.b.putTile(gridXY, player.color)
                    self.g.updateBoard(self.b)

            # TODO Fix Game flow

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







