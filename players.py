import pygame,sys
from pygame.locals import *
from random import choice
from const import *
import copy
import time
from scipy import optimize


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
            # count, move , timeTaken = self.minimax(self.board, self.color, 3, True)
            count, move , timeTaken = self.minimaxWalphaBeta(self.board, self.color, 3, -HUGE, HUGE, True)
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
            bestVal = -HUGE
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


    def minimaxWalphaBeta(self, board, color, depth, alpha, beta, maxPlayer, newMove=[]):
        if color == BLK:
            other = WHT
        else:
            other = BLK

        validMoves = board.getValidMoves(color)
        if depth == 0 or not validMoves or time.time() - self.startTime > self.timeOut:
            # TODO add proper heuristic
            return self.evalState(board, other), newMove, time.time() - self.startTime
        if maxPlayer:
            bestMove = (-1, -1)
            for move in validMoves:
                tempBoard = copy.deepcopy(board)
                tempBoard.putTile(move, color)
                val = self.minimaxWalphaBeta(tempBoard, other, depth-1, alpha, beta, False, move)[0]
                if val > alpha:
                    alpha = val
                    bestMove = move
                if beta <= alpha:
                    break
            return alpha, bestMove, time.time() - self.startTime
        else:
            bestMove = (-1, -1)
            for move in validMoves:
                tempBoard = copy.deepcopy(board)
                tempBoard.putTile(move,color)
                val = self.minimaxWalphaBeta(tempBoard, other, depth-1,alpha,beta, True, move)[0]
                if val < beta:
                    beta = val
                    bestMove = move
                if beta <=alpha:
                    break
            return beta, bestMove, time.time()- self.startTime


    def evalState(self, board, color):
        # Check
        # number of tiles
        # corner pieces
        # do you have more validMoves?
        tileCount = board.getTileCount()[tileMap[color]] # Gets number of tiles
        cornerCount = board.cornerCount[color]          # gets number of tiles in the corner
        edgeCount = board.edgeCount[color]
        moveCount = len(board.getValidMoves(color))

        return tileCount + 10*cornerCount + 3*edgeCount + 2*moveCount

