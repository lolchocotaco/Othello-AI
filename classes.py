# Class for board

from const import *
import numpy as np
import pygame,sys
from pygame.locals import  *

class Board:
    def __init__(self):
        self.board = np.zeros((8,8))
        self.board[3][4] = BLK
        self.board[4][3] = BLK
        self.board[3][3] = WHT
        self.board[4][4] = WHT
        self.validMoves = []

    def putTile(self,gridXY, color):
        if self.board[gridXY[1]][gridXY[0]] == EMP:
            self.board[gridXY[1]][gridXY[0]] = color


class GUI:
    def __init__(self):
        pygame.init()
        self.windowSize = 700
        self.spaceSize = 80
        self.boardSize = 8
        self.margin = int((self.windowSize - (self.boardSize * self.spaceSize)) / 2)
        self.boardWidth = self.windowSize-2*self.margin-10

        self.display = pygame.display.set_mode((self.windowSize,self.windowSize),0,32)
        self.display.fill(BLUE)
        pygame.display.set_caption('Chocotaco Othello')
        pygame.draw.rect(self.display,BG,(self.margin+5,self.margin+5,self.boardWidth,self.boardWidth))


    def updateBoard(self,b):
        for n,row in enumerate(b):
            # print(row)
            for m,cell in enumerate(row):
                pygame.draw.rect(self.display,GREEN,(self.margin+self.spaceSize*m+5,self.margin+self.spaceSize*n+5,self.spaceSize-10,self.spaceSize-10))
                if cell != EMP:
                    pygame.draw.circle(self.display, (cell == BLK)*BLACK+(cell == WHT)*WHITE, (int(self.margin+self.spaceSize*(0.5+m)), int(self.margin+self.spaceSize*(0.5+n))), 35, 0)
        pygame.display.flip()

    def getClick(self):
        while True: # Game Loop
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    (mouseX,mouseY) = pygame.mouse.get_pos()
                    # print([mouseX, mouseY])
                    # print(self.margin)
                    # print(self.boardSize)
                    if mouseX < self.margin or mouseY < self.margin or mouseX > self.margin+self.boardWidth or mouseY > self.margin+self.boardWidth:
                        continue

                    xPos = (mouseX - self.margin)/self.spaceSize
                    yPos = (mouseY - self.margin)/self.spaceSize
                    return([xPos,yPos])

