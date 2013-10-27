# Class for board

from const import *
import pygame,sys
import numpy
from pygame.locals import *
from board import Board
from gui import GUI
from players import *
from Tkinter import Tk
from tkFileDialog import askopenfilename


class Othello:
    def __init__(self):
        self.g = GUI()
        self.b = Board()
        self.players =[None, None]
        self.showMenu()

    def showMenu(self):
        # input =
        players, self.timeOut, setLayout = self.g.getPlayer()

        if players[0] == "h":
            self.players[0] = humanPlayer(BLK, self.g, self.b)
            self.players[1] = compPlayer(WHT, self.g,  self.b, self.timeOut)
        elif players[1] == "h":
            self.players[0] = compPlayer(BLK, self.g, self.b, self.timeOut)
            self.players[1] = humanPlayer(WHT, self.g, self.b)
        else:
            self.players[0] = compPlayer(BLK, self.g, self.b, self.timeOut)
            self.players[1] = compPlayer(WHT, self.g, self.b, self.timeOut)

        if setLayout:
            self.setLayout() # If a valid file isn't seleted the default layout is loaded
        self.g.showBoard()
        print("LET THE GAMES BEGIN!")

    def setLayout(self):
        Tk().withdraw()
        filename = askopenfilename()
        if filename:
            with open(filename, 'r') as f:
                board = numpy.genfromtxt(f,
                                         delimiter=' ',
                                         skip_footer=2,
                                         dtype=numpy.int32)
                self.b.board = board

            with open(filename,'r') as f2:
                options = numpy.genfromtxt(f2, delimiter=' ', dtype=numpy.int32,usecols=0, skip_header=8)
                self.timeOut = options[1]
                if options[0] == 2: # if 1 Black goes first, if 2 then white goes first.
                    self.players = self.players[::-1]


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
                    self.b.putTile(gridXY, player.color)
                    self.g.updateBoard(self.b)
                    # pygame.time.wait(int((200*self.timeOut+500)/7))

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







