import pygame,sys
from pygame.locals import *
from random import choice
from const import *

class Player():
    def __init__(self, color, gui):
        self.color = color
        self.gui = gui

    def getMove(self, validMoves):
        pass

    def flashTile(self,yPos,xPos):
        rectCord = self.gui.getSquare(yPos, xPos) # Get coordinates of thr square of the tile
        #Flash the tile
        for x in range(2):
            self.gui.putCircle(yPos, xPos,self.color)
            pygame.display.update(pygame.Rect(rectCord))
            pygame.time.wait(50)
            self.gui.drawTile(yPos,xPos,YELLOW)
            pygame.display.update(pygame.Rect(rectCord))
            pygame.time.wait(50)
        # pygame.time.wait(100)


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
                        continue

                    xPos = (mouseX - self.gui.margin)/self.gui.spaceSize
                    yPos = (mouseY - self.gui.margin)/self.gui.spaceSize

                    if (yPos, xPos) in validMoves:
                        self.flashTile(yPos,xPos)
                        return yPos, xPos


class compPlayer(Player):
    def getMove(self,validMoves):
        if validMoves:
            yPos,xPos = choice(validMoves)
            self.flashTile(yPos,xPos)
            return yPos, xPos