import pygame,sys
from pygame.locals import *
from random import choice
from const import *
import copy
import time

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
            self.startTime = time.time()
            count, move , timeTaken = self.minimax(self.board, self.color, 5, True)
            # yPos, xPos = choice(validMoves)
            print("Time taken: {0}").format(timeTaken)
            self.flashTile(move[0], move[1])
            return move

    def minimax(self, board, color, depth, maxPlayer, newMove=[]):
        if color == BLK:
            other = WHT
        else:
            other = BLK

        validMoves = board.getValidMoves(color)
        if depth == 0 or not validMoves or time.time()- self.startTime>self.timeOut:
            # TODO add proper heuristic
            return board.getTileCount()[tileMap[other]], newMove, time.time() - self.startTime
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
            return bestVal, bestMove, time.time()- self.startTime
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
            return bestVal, bestMove, time.time()- self.startTime
