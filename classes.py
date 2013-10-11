# Class for board

from const import BLK,WHT,EMP

class Board:
    def __init__(self):
        self.board = [[EMP for x in xrange(8)] for x in xrange(8)]
        self.board[3][4] = BLK
        self.board[4][3] = BLK
        self.board[3][3] = WHT
        self.board[4][4] = WHT