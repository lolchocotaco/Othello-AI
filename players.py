import pygame,sys
from pygame.locals import *
from random import choice

class Player():
    def __init__(self, color, gui):
        self.color = color
        self.gui = gui

    def getMove(self, validMoves):
        pass

class humanPlayer(Player):
    def getMove(self, validMoves):
         while True:  # Game Loop
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:

                    (mouseX, mouseY) = pygame.mouse.get_pos()
                    if mouseX < self.gui.margin or mouseY < self.gui.margin or mouseX > self.gui.margin+self.gui.boardWidth or mouseY > self.gui.margin+self.gui.boardWidth:
                        print("Continuing")
                        continue
                    print("clicked")

                    xPos = (mouseX - self.gui.margin)/self.gui.spaceSize
                    yPos = (mouseY - self.gui.margin)/self.gui.spaceSize
                    print(xPos,yPos)

                    if (yPos, xPos) in validMoves:
                        return yPos, xPos


class compPlayer(Player):
    def getMove(self,validMoves):
        if validMoves:
            return choice(validMoves)