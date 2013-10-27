import pygame,sys
from pygame.locals import *
from random import choice
from const import *
import copy

class Player():
    def __init__(self, color, gui,board):
        self.color = color
        self.gui = gui
        self.board = board

    def getMove(self, validMoves):
        pass

    def flashTile(self, yPos, xPos):
        rectCord = self.gui.getSquare(yPos, xPos) # Get coordinates of thr square of the tile
        #Flash the tile
        for x in range(2):
            self.gui.putCircle(yPos, xPos,self.color)
            pygame.display.update(pygame.Rect(rectCord))
            pygame.time.wait(100)
            self.gui.drawTile(yPos,xPos,YELLOW)
            pygame.display.update(pygame.Rect(rectCord))
            pygame.time.wait(100)
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
    def __init__(self, color, gui, board, timeOut):
        self.color = color
        self.gui = gui
        self.board = board
        self.timeOut = timeOut

    def getMove(self,validMoves):
        if validMoves:

            yPos,xPos = self.minimax(self.board, self.color, 3, True)[1]
            # yPos, xPos = choice(validMoves)
            self.flashTile(yPos, xPos)
            return yPos, xPos

    def minimax(self, board, color, depth, maxPlayer, newMove=[]):
        if color == BLK:
            other = WHT
        else:
            other = BLK

        validMoves = board.getValidMoves(color)
        if depth == 0 or not validMoves:
            return board.getTileCount()[tileMap[other]], newMove
        if maxPlayer:
            bestVal= -HUGE
            bestMove = (-1, -1)
            for move in validMoves:
                tempBoard = copy.deepcopy(board)
                tempBoard.putTile(move, color)
                val = self.minimax(tempBoard, other, depth-1, False, move)[0]
                if val > bestVal:
                    bestVal = val
                    bestMove = move
            return bestVal, bestMove
        else:
            bestVal = HUGE
            bestMove = (-1, -1)
            for move in validMoves:
                tempBoard = copy.deepcopy(board)
                tempBoard.putTile(move,color)
                val = self.minimax(tempBoard, other, depth-1, True, move)[0]
                if val < bestVal:
                    bestVal = val
                    bestMove = move
            return bestVal, bestMove
