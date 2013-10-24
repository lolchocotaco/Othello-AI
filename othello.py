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
        players, self.timeout,setLayout = self.g.getPlayer()
        print (setLayout)
        if players[0] == "h":
            self.players[0] = humanPlayer(BLK, self.g)
            self.players[1] = compPlayer(WHT, self.g)
        elif players[1] == "h":
            self.players[0] = compPlayer(BLK, self.g)
            self.players[1] = humanPlayer(WHT, self.g)
        else:
            self.players[0] = compPlayer(BLK, self.g)
            self.players[1] = compPlayer(WHT, self.g)
        self.g.showBoard()
        if setLayout:
            self.setLayout()
        print("LET THE GAMES BEGIN!")

    def setLayout(self):
        # TODO Change to load file.
        while True:
            n, m = self.g.getClick()
            self.g.putCircle(n,m,BLK)
            pygame.display.flip()

    def play(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.display.quit()
                        sys.exit()
        # Get valid  moves and make moves
            for player in self.players:
                validMoves = self.b.getValidMoves(player.color)  # Get list of valid moves
                if validMoves:
                    self.g.updateBoard(self.b, player.color) # Update board to show possible moves
                    gridXY = player.getMove(validMoves)
                    # pygame.time.wait(int((200*self.timeout+500)/7))
                    self.b.putTile(gridXY, player.color)
                    self.g.updateBoard(self.b)

            # Check end state
            if self.b.checkEnd():
                    print("Game ended")
                    tileCount = self.b.getTileCount()
                    print(tileCount)
                    if tileCount[0] > tileCount[1]:
                        self.g.showWinner(BLK)
                        print("Black wins")
                    elif tileCount[0]< tileCount[1]:
                        self.g.showWinner(WHT)
                        print("White wins")
                    else:
                        print("Magically a draw")
                    pygame.time.wait(5000)
                    pygame.quit()
                    sys.exit()







