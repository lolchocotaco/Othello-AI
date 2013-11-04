from random import choice
import numpy as np
# cimport numpy as np
from const import *
from collections import defaultdict
import itertools
cimport cython

class Board:

    def __init__(self):
        self.board = np.zeros((8,8), dtype=np.int)
        self.board[3, 4] = BLK
        self.board[4, 3] = BLK
        self.board[3, 3] = WHT
        self.board[4, 4] = WHT
        self.validMoves = defaultdict()
        self.validMoves[BLK] = [] #np.empty([1,1],dtype=tuple)
        self.validMoves[WHT] = [] #np.empty([1,1],dtype=tuple)
        self.validMoves[EMP] = [] #np.empty([1,1],dtype=tuple)
        self.cornerCount = defaultdict()
        self.edgeCount = defaultdict()
        self.cornerClose = defaultdict()

    def putTile(self, gridXY, int color):
        if self.board[gridXY[0], gridXY[1]] == EMP:
            self.board[gridXY[0], gridXY[1]] = color
            for x in range(8):
                self.flip(gridXY, color,x)

    # def getValidMoves(self, color):
    #     moves = [self.getMoves(pos,pos2,cell) for (pos, pos2), cell in np.ndenumerate(self.board) if cell == color]
    #     self.validMoves[color] = list(itertools.chain(*moves))
    #     return self.validMoves[color]
    #
    def getValidMoves(self, int color):
        moves = []
        # Check all elements
        cdef int n,m, cell
        # cdef np.ndarray[np.int_t, ndim=1] row = np.empty(8, dtype=np.int)
        for (n,m), cell in np.ndenumerate(self.board):
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
        count = defaultdict()
        count[BLK] = 0
        count[WHT] = 0
        self.cornerCount[BLK] = 0
        self.cornerCount[WHT] = 0
        self.edgeCount[BLK] = 0
        self.edgeCount[WHT] = 0
        self.cornerClose[BLK] = 0
        self.cornerClose[WHT] = 0

        # # [pos,pos2,cell for (pos, pos2), cell in np.ndenumerate(self.board)if cell != EMP]
        # occupied = [[(pos,pos2),cell] for (pos,pos2),cell in np.ndenumerate(self.board) if cell != EMP]
        # blkTiles = filter(lambda x:x[1] == BLK,occupied)
        # whtTiles = filter(lambda x:x[1] == WHT, occupied)
        # count[BLK] = len(blkTiles)
        # count[WHT] = len(whtTiles)
        #
        # self.edgeCount[BLK] = len(filter(lambda x: 0 in x[0] or 7 in x[0], blkTiles))
        # self.edgeCount[WHT] = len(filter(lambda x: 0 in x[0] or 7 in x[0], whtTiles))
        cdef int rowNum,colNum
        cdef int cell

        for (rowNum,colNum), cell in np.ndenumerate(self.board):
            if cell != EMP:
                count[cell] += 1
                if colNum == 0 or colNum == 7 or rowNum == 0 or rowNum == 7:
                    self.edgeCount[cell] += 1
                if (rowNum, colNum) in [(0, 0), (0, 7), (7, 7), (7, 0)]:
                    self.cornerCount[cell] += 1
                if (rowNum,colNum) in [(1, 0), (0, 1), (1, 1), (7, 6), (6, 6), (6, 7), (6, 0), (6, 1), (7, 1), (0, 6), (1, 6), (1, 7)]:
                    self.cornerClose[cell] +=1

        return count[BLK], count[WHT]


    # Indexing will work properly
    @cython.boundscheck(False)
    @cython.wraparound(False)
    def getMoves(self, int inRow, int inCol, int color):
        cdef int n  = inRow
        cdef int m = inCol

        cdef int row, col, colI, rowI, other

        if color == BLK:
            other = WHT
        else:
            other = BLK
        moveList = []
        row = n
        col = m

        for rowI in range(-1,2, 1):
            for colI in range(-1,2,1):
                n = row
                m = col
                if n+rowI >7 or m+colI > 7 or n+rowI < 0 or m+colI< 0:
                    continue
                if n in range(8) and m in range(8) and self.board[n+rowI, m+colI] == other:
                    n += rowI
                    m += colI
                    while n in range(8) and m in range(8) and self.board[n, m] == other:
                        if n+rowI >7 or m+colI > 7 or n+rowI < 0 or m+colI< 0:
                            break
                        if self.board[n+rowI, m+colI] == EMP:
                            moveList = moveList + [(n+rowI, m+colI)]
                            break
                        n += rowI
                        m += colI
        return moveList

    def flip(self, gridXY, int color, int dir):

        cdef int other,row,col,n,m, rowI, colI

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
        else:
            return flipPos

        #Begin the flipping process
        row = gridXY[0]
        col = gridXY[1]

        n = row+rowI
        m = col+colI

        while n in range(8) and m in range(8) and self.board[n,m] == other:
            flipPos = flipPos + [(n, m)]
            n += rowI
            m += colI

        if n in range(8) and m in range(8) and self.board[n,m] == color:
            for pos in flipPos:
                self.board[pos[0], pos[1]] = color


    # Not used
    def makeCompMove(self,color):
        validMoves = self.getValidMoves(color)
        if validMoves:
            self.putTile(choice(validMoves), color)
