from random import choice
import numpy as np
from const import *
from collections import defaultdict
import itertools
import cython



class Board:
    def __init__(self):
        self.board = np.zeros((8,8), dtype=np.int32)
        self.board[3, 4] = BLK
        self.board[4, 3] = BLK
        self.board[3, 3] = WHT
        self.board[4, 4] = WHT
        self.validMoves = defaultdict()
        self.validMoves[BLK] = []
        self.validMoves[WHT] = []
        self.validMoves[EMP] = []
        self.cornerCount = defaultdict()
        self.edgeCount = defaultdict()

    def putTile(self, gridXY, color):
        if self.board[gridXY[0], gridXY[1]] == EMP:
            self.board[gridXY[0], gridXY[1]] = color
            for x in range(8):
                self.flip(gridXY, color,x)

    # def getValidMoves(self, color):
    #     moves = [self.getMoves(pos,pos2,cell) for (pos, pos2), cell in np.ndenumerate(self.board) if cell == color]
    #     self.validMoves[color] = list(itertools.chain(*moves))
    #     return self.validMoves[color]

    def getValidMoves(self, color):
        moves = []
        # Check all elements
        for n, row in enumerate(self.board):
            for m, cell in enumerate(row):
                if cell == color:
                    moves = moves + self.getMoves(n, m, color)
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
        count = defaultdict()
        count[BLK] = 0
        count[WHT] = 0
        self.cornerCount[BLK] = 0
        self.cornerCount[WHT] = 0
        self.edgeCount[BLK] = 0
        self.edgeCount[WHT] = 0

        # # [pos,pos2,cell for (pos, pos2), cell in np.ndenumerate(self.board)if cell != EMP]
        # occupied = [[(pos,pos2),cell] for (pos,pos2),cell in np.ndenumerate(self.board) if cell != EMP]
        # blkTiles = filter(lambda x:x[1] == BLK,occupied)
        # whtTiles = filter(lambda x:x[1] == WHT, occupied)
        # count[BLK] = len(blkTiles)
        # count[WHT] = len(whtTiles)
        #
        # self.edgeCount[BLK] = len(filter(lambda x: 0 in x[0] or 7 in x[0], blkTiles))
        # self.edgeCount[WHT] = len(filter(lambda x: 0 in x[0] or 7 in x[0], whtTiles))

        for rowNum, row in enumerate(self.board):
            for colNum, cell in enumerate(row):
                if cell != EMP:
                    count[cell] += 1
                    if colNum == 0 or colNum == 7 or rowNum == 0 or rowNum == 7:
                        self.edgeCount[cell] += 1
                    if (rowNum, colNum) in [(0, 0), (0, 7), (7, 7), (7, 0)]:
                        # print("Corner found {0}-{1}").format(rowNum, colNum)
                        self.cornerCount[cell] += 1
        return count[BLK], count[WHT]

    def getMoves(self, n, m, color):
        if color == BLK:
            other = WHT
        else:
            other = BLK
        moveList = []
        row = n
        col = m

        for rowI in [-1, 0, 1]:
            for colI in [-1, 0 ,1]:
                n = row
                m = col
                if n+rowI >7 or m+colI > 7 or n+rowI < 0 or m+colI< 0:
                    continue
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

    def flip(self,gridXY,color, dir):

        flipPos = []
        if color == BLK:
            other = WHT
        else:
            other = BLK
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
            flipPos = flipPos + [(n, m)]
            n += rowI
            m += colI

        if n in range(8) and m in range(8) and self.board[n][m] == color:
            for pos in flipPos:
                self.board[pos[0]][pos[1]] = color


    # Not used
    def makeCompMove(self,color):
        validMoves = self.getValidMoves(color)
        if validMoves:
            self.putTile(choice(validMoves), color)
