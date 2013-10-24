import pygame,sys
import pygame.gfxdraw
from pygame.locals import *
from const import *
from menu import Menu

class GUI:
    def __init__(self):
        pygame.init()
        self.windowSize = 800
        self.spaceSize = 80
        self.boardSize = 8
        self.margin = int((self.windowSize - (self.boardSize * self.spaceSize)) / 2)
        self.boardWidth = self.windowSize - 2*self.margin-10

        self.display = pygame.display.set_mode((self.windowSize,self.windowSize),0,32)
        self.display.fill(GREY)
        pygame.display.set_caption('Chocotaco Othello')

        # font stuff
        self.font = pygame.font.Font('font/coders_crux.ttf', 32)
        self.titleFont = pygame.font.Font('font/coders_crux.ttf',64)
        self.titleFont.set_bold(True)
        self.scorePosB = (self.windowSize/4, 50 )
        self.scorePosW = (int(3*self.windowSize/4), 50)


    def showBoard(self):
        self.display.fill(BLUE)
        pygame.draw.rect(self.display, BG, (self.margin+5, self.margin+5, self.boardWidth, self.boardWidth))
        blkText = self.font.render("Black: ", True, BLACK, BLUE)
        whtText = self.font.render("White: ", True, WHITE, BLUE)
        self.display.blit(blkText, (self.scorePosB[0]- 70, self.scorePosB[1] ))
        self.display.blit(whtText, (self.scorePosW[0]- 70, self.scorePosW[1] ))


    def getPlayer(self):
        # Starting screen text
        title = self.titleFont.render("Chocotaco Othello",True,DULLYELLOW)
        self.display.blit(title,(int(self.boardWidth/4),50))
        info = [None]*4
        info[0] = self.font.render("Select playing option using the UP & DOWN arrow keys.", True, WHITE)
        info[1] = self.font.render("Set computer timeout using the LEFT & RIGHT arrow keys",True, WHITE)
        info[2] = self.font.render("Make a selection using the ENTER key", True,WHITE)
        info[3] = self.font.render("To specify board layout, make selection using SPACE.", True, WHITE)
        for n,blurb in enumerate(info):
            self.display.blit(blurb,(75,self.boardWidth/4+32*n))
        #Time out information
        timeOut = 5
        timeOutLabel = self.font.render("Timeout", True, WHITE)
        self.display.blit(timeOutLabel,(int(3*self.windowSize/4)+16, int(self.boardWidth/2)+32))
        self.showTimeout(timeOut)
        #Actual Menu
        menu = Menu()
        menu.init(['Go First (Black)', 'Go Second (White)','Comp V Comp', 'Quit'], self.display)
        menu.draw()
        pygame.key.set_repeat(199,69)
        pygame.display.update()
        while 1:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        if timeOut >1:
                            timeOut -= 1
                            self.showTimeout(timeOut)
                    elif event.key == K_RIGHT:
                        if timeOut < 15:
                            timeOut += 1
                            self.showTimeout(timeOut)
                    elif event.key == K_UP:
                        menu.draw(-1) #here is the Menu class function
                    elif event.key == K_DOWN:
                        menu.draw(1) #here is the Menu class function
                    elif event.key == K_RETURN or event.key == K_SPACE:
                        if menu.get_position() == 0:
                            return ["h", "c"], timeOut, (event.key == K_SPACE)
                        elif menu.get_position() == 1:
                            return ["c", "h"], timeOut, (event.key == K_SPACE)
                        elif menu.get_position() == 2:
                            return ["c", "c"], timeOut, (event.key == K_SPACE)
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

    def showTimeout(self,timeout):
        timeOutTxt = self.font.render(str(timeout).rjust(2,'0')+" Seconds",True,LIGHTBLUE,GREY)
        self.display.blit(timeOutTxt, (int(3*self.windowSize/4), int(self.boardWidth/2)+64))


    def updateBoard(self,boardClass, color=EMP):
        board = boardClass.board
        validMoves = boardClass.validMoves[color]
        blkCount = 0
        whtCount =0
        for n, row in enumerate(board):
            # print(row)
            for m,cell in enumerate(row):
                # pygame.draw.rect(self.display, GREEN, (self.margin+self.spaceSize*m+5,self.margin+self.spaceSize*n+5,self.spaceSize-10,self.spaceSize-10))
                self.drawTile(n,m,GREEN)
                if (n, m) in validMoves:
                    # pygame.draw.rect(self.display, YELLOW, (self.margin+self.spaceSize*m+5,self.margin+self.spaceSize*n+5,self.spaceSize-10,self.spaceSize-10))
                    self.drawTile(n,m,YELLOW)

                if cell != EMP:
                    blkCount += (cell == BLK)*1
                    whtCount += (cell == WHT)*1
                    # pygame.draw.circle(self.display, (cell == BLK)*BLACK+(cell == WHT)*WHITE, (int(self.margin+self.spaceSize*(0.5+m)), int(self.margin+self.spaceSize*(0.5+n))), 35, 0)
                    # Anti aliased circles act weird on top of each other
                    # pygame.gfxdraw.aacircle(self.display, int(self.margin+self.spaceSize*(0.5+m)), int(self.margin+self.spaceSize*(0.5+n)), 35,  (cell == BLK)*BLACK+(cell == WHT)*WHITE)
                    # pygame.gfxdraw.filled_circle(self.display, int(self.margin+self.spaceSize*(0.5+m)), int(self.margin+self.spaceSize*(0.5+n)), 35,  (cell == BLK)*BLACK+(cell == WHT)*WHITE)
                    self.putCircle(n, m, cell)

        #Showing score
        blkScore = self.font.render(str(blkCount).rjust(2,'0'), True, BLACK,BLUE)
        whtScore = self.font.render(str(whtCount).rjust(2,'0'), True, WHITE,BLUE)
        self.display.blit(blkScore, self.scorePosB)
        self.display.blit(whtScore, self.scorePosW)
        pygame.display.flip()

    def getSquare(self,n,m):
        return (self.margin+self.spaceSize*m+5,self.margin+self.spaceSize*n+5,self.spaceSize-10,self.spaceSize-10)

    def putCircle(self, n, m, color):
        pygame.gfxdraw.filled_circle(self.display, int(self.margin+self.spaceSize*(0.5+m)), int(self.margin+self.spaceSize*(0.5+n)), 35,  (color == BLK)*BLACK+(color == WHT)*WHITE)

    def drawTile(self, n, m, tileColor):
        pygame.draw.rect(self.display, tileColor, (self.margin+self.spaceSize*m+5,self.margin+self.spaceSize*n+5,self.spaceSize-10,self.spaceSize-10))

    def getClick(self):
        while True:  # Game Loop
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        pygame.quit()
                        sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    (mouseX, mouseY) = pygame.mouse.get_pos()
                    if mouseX < self.margin or mouseY < self.margin or mouseX > self.margin+self.boardWidth or mouseY > self.margin+self.boardWidth:
                        continue

                    xPos = (mouseX - self.margin)/self.spaceSize
                    yPos = (mouseY - self.margin)/self.spaceSize
                    return yPos, xPos

    def click2Grid(self,gridXY):
        x = gridXY[0]
        y = gridXY[1]
        if x < self.margin or y < self.margin or x > self.margin+self.boardWidth or y > self.margin+self.boardWidth:
                return -1,-1

        xPos = (x - self.margin)/self.spaceSize
        yPos = (x - self.margin)/self.spaceSize
        return yPos,xPos


    def showWinner(self,color):
        if color == BLK:
            winnerText = self.font.render("Black Wins!!", True, BLACK,BLUE)
        elif color == WHT:
            winnerText = self.font.render("White Wins!!", True, WHITE,BLUE)
        else:
            winnerText = self.font.render("Its a DRAW!!", True, GREY,BLUE)
        self.display.blit(winnerText,(self.boardWidth/2, 50 ))
        pygame.display.flip()