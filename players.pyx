import pygame,sys
from pygame.locals import *
from random import choice
from const import *
import copy
import time
import cython
cimport cython
# from cython cimport bool







class Player:

    def __init__(self, int color, gui,board):
        self.color = color
        self.gui = gui
        self.board = board

    def getMove(self, validMoves):
        pass

    def flashTile(self, int yPos, int xPos):
        rectCord = self.gui.getSquare(yPos, xPos) # Get coordinates of thr square of the tile
        #Flash the tile
        for x in range(2):
            self.gui.putCircle(yPos, xPos,self.color)
            pygame.display.update(pygame.Rect(rectCord))
            pygame.time.wait(100)
            self.gui.drawTile(yPos,xPos,GREEN)
            pygame.display.update(pygame.Rect(rectCord))
            pygame.time.wait(100)
        # pygame.time.wait(100)


class humanPlayer(Player):
    def __init__(self, color, gui, board):
        Player.__init__(self, color, gui, board)
        self.isBot = False

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
        Player.__init__(self, color, gui, board)
        self.timeOut = timeOut
        self.isBot = True

    def getMove(self,validMoves):
        if validMoves: #If only one move, choose it
            if len(validMoves) == 1:
                return validMoves[0]
            self.startTime = time.time()
            # count, move , timeTaken = self.minimax(self.board, self.color, 3, True)
            # count, move , timeTaken = self.minimaxWalphaBeta(self.board, self.color, 3, -HUGE, HUGE, True)
            depth = 0
            bestMove = []
            score = -HUGE
            # Do not look at next depth if more than half of timeout
            while time.time() - self.startTime < self.timeOut/2.0:
                depth += 1
                count, move, timeTaken= self.minimaxWalphaBeta(self.board, self.color, depth, -HUGE, HUGE, True)
                if move and count> score: # Need to check count because partial check of last depth would return a bad value
                    score = count
                    bestMove = move

            if not bestMove:
                print("Could not find any moves, but this shouldn't be happening..")
                print("Program died.... exiting")
                sys.exit()
                pygame.quit()

            print("Time taken: {0} to depth: {1} with score {2}").format(round(timeTaken,2), depth, round(score,2))
            self.flashTile(bestMove[0], bestMove[1])
            return bestMove

    def minimaxWalphaBeta(self, board, int color, int depth, int alpha, int beta,  maxPlayer, tuple bestMove=()):
        cdef int other, val
        cdef tuple move

        if color == BLK:
            other = WHT
        else:
            other = BLK


        # keep track of self.color
        validMoves = board.getValidMoves(color)
        # if depth == 0 or not validMoves or time.time() - self.startTime > self.timeOut:
        if time.time() - self.startTime > 7*self.timeOut/8.0:
            return -HUGE, [], 0
        if depth == 0 or not validMoves: # or time.time()-self.startTime > 3*self.timeOut/4.0:
            # TODO add proper heuristic
            return self.evalState(board, self.color), bestMove, time.time()-self.startTime
        if maxPlayer:
            for move in validMoves:
                tempBoard = copy.deepcopy(board)
                tempBoard.putTile(move, color)
                val = self.minimaxWalphaBeta(tempBoard, other, depth-1, alpha, beta, False, move)[0]
                if val > alpha:
                    alpha = val
                    bestMove = move
                if beta <= alpha:
                    break
                    # pass
                # print("{0}Move {1} with score: {2}").format("\t"*(4-depth),move, alpha)
            return alpha, bestMove, time.time() - self.startTime
        else:
            for move in validMoves:
                tempBoard = copy.deepcopy(board)
                tempBoard.putTile(move, color)
                val = self.minimaxWalphaBeta(tempBoard, other, depth-1, alpha, beta, True, move)[0]
                if val < beta:
                    beta = val
                    bestMove = move
                if beta <= alpha:
                    break
                    # pass
                # print("{0}Move {1} with score: {2}").format("\t"*(4-depth),move, beta)
            return beta, bestMove, time.time() - self.startTime


    def evalState(self, board, color):
        if color == BLK:
            other = WHT
        else:
            other = BLK

        tileCount = board.getTileCount()
        # Piece differential

        if tileCount[tileMap[color]] != tileCount[tileMap[other]]:
            scoreDiff = 100 * (tileCount[tileMap[color]] - tileCount[tileMap[other]] )/(1.0*(tileCount[tileMap[color]] + tileCount[tileMap[other]]))
        else:
            scoreDiff = 0

        scoreCorner = 100*board.cornerCount[color] - 100*board.cornerCount[other]

        maxMoveCount = len(board.getValidMoves(color))
        minMoveCount = len(board.getValidMoves(other))
        if maxMoveCount != minMoveCount:
            scoreMove = 100 * (maxMoveCount - minMoveCount)/(1.0*(maxMoveCount + minMoveCount))
        else:
            scoreMove = 0

        return scoreDiff + 50 * scoreCorner + scoreMove

    def evalState2(self, board, color):
        # Check
        # number of tiles
        # corner pieces
        # do you have more validMoves?
        tileCount = board.getTileCount()[tileMap[color]] # Gets number of tiles
        if tileCount == 0:
            return -HUGE
        elif tileCount == 64:
            return HUGE
        cornerCount = board.cornerCount[color]          # gets number of tiles in the corner
        edgeCount = board.edgeCount[color]
        moveCount = len(board.getValidMoves(color))

        return tileCount + 16*cornerCount + 3*edgeCount + 2*moveCount



    # bad minimax that no one uses
    def minimax(self, board, color, depth, maxPlayer, newMove=[]):
        if color == BLK:
            other = WHT
        else:
            other = BLK

        validMoves = board.getValidMoves(color)
        # if depth == 0 or not validMoves or time.time()- self.startTime>self.timeOut:
        if not validMoves or time.time()- self.startTime>self.timeOut:
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


                # def minimaxWalphaBeta(self, board, color, depth, alpha, beta, maxPlayer, newMove=[]):

