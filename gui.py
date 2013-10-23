import pygame,sys
from pygame.locals import *
from const import *
from menu import Menu

class GUI:
    def __init__(self):
        pygame.init()
        self.windowSize = 700
        self.spaceSize = 80
        self.boardSize = 8
        self.margin = int((self.windowSize - (self.boardSize * self.spaceSize)) / 2)
        self.boardWidth = self.windowSize - 2*self.margin-10

        self.display = pygame.display.set_mode((self.windowSize,self.windowSize),0,32)
        self.display.fill(GREY)
        pygame.display.set_caption('Chocotaco Othello')

    def showBoard(self):
        self.display.fill(BLUE)
        pygame.draw.rect(self.display, BG, (self.margin+5, self.margin+5, self.boardWidth, self.boardWidth))

    def getPlayer(self):
        menu = Menu()
        menu.init(['Go First (Black)', 'Go Second (White)','Comp V Comp', 'Quit'], self.display)
        menu.draw()
        pygame.key.set_repeat(199,69)
        pygame.display.update()
        while 1:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        menu.draw(-1) #here is the Menu class function
                    if event.key == K_DOWN:
                        menu.draw(1) #here is the Menu class function
                    if event.key == K_RETURN:
                        if menu.get_position() ==0:
                            return BLK, WHT, False
                        elif menu.get_position() == 1:
                            return WHT, BLK, False
                        elif menu.get_position() == 2:
                            return BLK, WHT, True
                        elif menu.get_position() == 3:#here is the Menu class function
                            pygame.display.quit()
                            sys.exit()
                    if event.key == K_ESCAPE:
                        pygame.display.quit()
                        sys.exit()
                    pygame.display.update()
                elif event.type == QUIT:
                    pygame.display.quit()
                    sys.exit()


    def updateBoard(self,boardClass, color=EMP):
        board = boardClass.board
        validMoves = boardClass.validMoves[color]
        for n, row in enumerate(board):
            # print(row)
            for m,cell in enumerate(row):
                pygame.draw.rect(self.display, GREEN, (self.margin+self.spaceSize*m+5,self.margin+self.spaceSize*n+5,self.spaceSize-10,self.spaceSize-10))
                if (n,m) in validMoves:
                    pygame.draw.rect(self.display, YELLOW, (self.margin+self.spaceSize*m+5,self.margin+self.spaceSize*n+5,self.spaceSize-10,self.spaceSize-10))

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
