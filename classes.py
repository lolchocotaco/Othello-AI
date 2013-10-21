# Class for board

from const import *
import numpy as np
import pygame,sys
from pygame.locals import *
from random import choice


class Board:
    def __init__(self):
        self.board = np.zeros((8,8))
        self.board[3][4] = BLK
        self.board[4][3] = BLK
        self.board[3][3] = WHT
        self.board[4][4] = WHT

    def putTile(self, gridXY, color):
        if self.board[gridXY[0]][gridXY[1]] == EMP:
            self.board[gridXY[0]][gridXY[1]] = color
            for x in range(8):
                self.flip(x, gridXY, color)

    def getValidMoves(self, color):
        moves = []
        # Check all elements
        for n, row in enumerate(self.board):
            for m, cell in enumerate(row):
                if cell == color:
                    for dir in range(8):
                        moves = moves + self.getMoves(n, m, color,dir)

        return moves

    def getMoves(self, n, m, color, dir):
        if color == BLK:
            other = WHT
        else:
            other = BLK

        moveList = []
        row = n
        col = m

        if dir == 0:
            rowI = -1
            colI = 0
         # S
        elif dir == 1:
            rowI = 1
            colI = 0
         # W
        elif dir == 2:
            rowI = 0
            colI =-1
        # E
        elif dir == 3:
            rowI = 0
            colI = 1
        # NW
        elif dir == 4:
            rowI = -1
            colI = -1
        # NE
        elif dir == 5:
            rowI = -1
            colI = 1
        # SW
        elif dir == 6:
            rowI = 1
            colI = -1
        # SE
        elif dir == 7:
            rowI = 1
            colI = 1

        if n in range(1,7) and m in range(1,7) and self.board[n+rowI][m+colI] == other:
            n += rowI
            m += colI
            while n in range(1,7) and m in range(1,7) and self.board[n][m] == other:
                if self.board[n+rowI][m+colI] == EMP:
                    moveList = moveList + [(n+rowI, m+colI)]
                    break
                n += rowI
                m += colI
        return moveList

    def flip(self,dir,gridXY,color):

        flipPos = []
        if color == BLK:
            other = WHT
        else:
            other = BLK

        # N
        if dir == 0:
            rowI = -1
            colI = 0
         # S
        elif dir == 1:
            rowI = 1
            colI = 0
         # W
        elif dir == 2:
            rowI = 0
            colI =-1
        # E
        elif dir == 3:
            rowI = 0
            colI = 1
        # NW
        elif dir == 4:
            rowI = -1
            colI = -1
        # NE
        elif dir == 5:
            rowI = -1
            colI = 1
        # SW
        elif dir == 6:
            rowI = 1
            colI = -1
        # SE
        elif dir == 7:
            rowI = 1
            colI = 1

        #Begin the flipping process
        row = gridXY[0]
        col = gridXY[1]

        n = row+rowI
        m = col+colI

        while n in range(8) and m in range(8) and self.board[n][m] == other:
            flipPos = flipPos + [(n,m)]
            n += rowI
            m += colI

        if n in range(8) and m in range(8) and self.board[n][m] == color:
            for pos in flipPos:
                self.board[pos[0]][pos[1]] = color



    def makeCompMove(self,color):
        validMoves = self.getValidMoves(color)
        if validMoves:
            self.putTile(choice(validMoves), color)


class GUI:
    def __init__(self):
        pygame.init()
        self.windowSize = 700
        self.spaceSize = 80
        self.boardSize = 8
        self.margin = int((self.windowSize - (self.boardSize * self.spaceSize)) / 2)
        self.boardWidth = self.windowSize - 2*self.margin-10

        self.display = pygame.display.set_mode((self.windowSize,self.windowSize),0,32)
        self.display.fill(BLUE)
        pygame.display.set_caption('Chocotaco Othello')
        pygame.draw.rect(self.display, BG, (self.margin+5, self.margin+5, self.boardWidth, self.boardWidth))

    def updateBoard(self,board):
        pygame.time.wait(10)
        for n, row in enumerate(board):
            # print(row)
            for m,cell in enumerate(row):
                pygame.draw.rect(self.display, GREEN, (self.margin+self.spaceSize*m+5,self.margin+self.spaceSize*n+5,self.spaceSize-10,self.spaceSize-10))
                if cell != EMP:
                    pygame.draw.circle(self.display, (cell == BLK)*BLACK+(cell == WHT)*WHITE, (int(self.margin+self.spaceSize*(0.5+m)), int(self.margin+self.spaceSize*(0.5+n))), 35, 0)
        pygame.display.flip()

    def getClick(self):
        while True:  # Game Loop
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    (mouseX, mouseY) = pygame.mouse.get_pos()
                    if mouseX < self.margin or mouseY < self.margin or mouseX > self.margin+self.boardWidth or mouseY > self.margin+self.boardWidth:
                        continue

                    xPos = (mouseX - self.margin)/self.spaceSize
                    yPos = (mouseY - self.margin)/self.spaceSize
                    return yPos, xPos

