from random import choice
import numpy as np
from const import *
from collections import defaultdict

class Board:
    def __init__(self):
        self.board = np.zeros((8,8))
        self.board[3][4] = BLK
        self.board[4][3] = BLK
        self.board[3][3] = WHT
        self.board[4][4] = WHT
        self.validMoves = defaultdict()
        self.validMoves[BLK] = []
        self.validMoves[WHT] =[]
        self.validMoves[EMP] = []

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
                        moves = moves + self.getMoves(n, m, color, dir)
        self.validMoves[color] = list(set(moves))
        return self.validMoves[color]

    def checkEnd(self):
        if self.validMoves[BLK] or self.validMoves[WHT]:
            return False
        else:
            return True

    def getTileCount(self):
        blkCount = 0
        whtCount = 0
        for row in self.board:
            for cell in row:
                if cell == BLK:
                    blkCount += 1
                elif cell == WHT:
                    whtCount += 1
        return blkCount, whtCount

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

        if n+rowI >7 or m+colI > 7 or n+rowI < 0 or m+colI< 0:
            return moveList
        if n in range(8) and m in range(8) and self.board[n+rowI][m+colI] == other:
            n += rowI
            m += colI
            while n in range(8) and m in range(8) and self.board[n][m] == other:
                if n+rowI >7 or m+colI > 7 or n+rowI < 0 or m+colI< 0:
                    break
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