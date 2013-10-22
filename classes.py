# Class for board

from const import *
import numpy as np
import pygame,sys
from pygame.locals import *
from random import choice
from collections import defaultdict


class Othello:
    def __init__(self):
        self.g = GUI()
        self.b = Board()
        self.showMenu()

    def showMenu(self):
        # input =
        self.player1, self.player2 = self.g.getPlayer()
        print("LET THE GAMES BEGIN!")
        self.g.showBoard()

    def play(self):
        while True:
        # Get valid black moves
            validMoves = self.b.getValidMoves(self.player1)
            self.g.updateBoard(self.b, self.player1)
            # If there are any valid moves get Clicks
            if validMoves:
                gridXY = self.g.getClick()
                # print(gridXY)
                # If the click is in the valid --> Put tile, and let computer make moves
                if gridXY in validMoves:
                    self.b.putTile(gridXY, self.player1)
                    self.g.updateBoard(self.b)
                    pygame.time.wait(500)
                    self.b.makeCompMove(self.player2)
                    self.g.updateBoard(self.b)
            else:
                print("No valid Moves.. you skipped")
                self.b.makeCompMove(self.player2)
                self.g.updateBoard(self.b, self.player2)

            # TODO Fix game flow. Possibly wrap game in another othello class


            # Check end state
            if self.b.checkEnd():
                    print("Game ended")
                    tileCount = self.b.getTileCount()
                    print(tileCount)
                    if tileCount[0] > tileCount[1]:
                        print("Black wins")
                    elif tileCount[0]< tileCount[1]:
                        print("White wins")
                    else:
                        print("Magically a draw")
                    pygame.time.wait(5000)
                    pygame.quit()
                    sys.exit()



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

    def getValidMoves(self,color):
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
        menu.init(['Black', 'White', 'Quit'], self.display)
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
                            return BLK, WHT
                        if menu.get_position() ==1:
                            return WHT, BLK
                        elif menu.get_position() == 2:#here is the Menu class function
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



class Menu:
    lista = []
    pola = []
    rozmiar_fontu = 32
    font_path = 'font/coders_crux.ttf'
    font = pygame.font.Font
    dest_surface = pygame.Surface
    ilosc_pol = 0
    kolor_tla = (51,51,51)
    kolor_tekstu =  (255, 255, 153)
    kolor_zaznaczenia = (153,102,255)
    pozycja_zaznaczenia = 0
    pozycja_wklejenia = (0,0)
    menu_width = 0
    menu_height = 0

    class Pole:
        tekst = ''
        pole = pygame.Surface
        pole_rect = pygame.Rect
        zaznaczenie_rect = pygame.Rect

    def move_menu(self, top, left):
        self.pozycja_wklejenia = (top,left)

    def set_colors(self, text, selection, background):
        self.kolor_tla = background
        self.kolor_tekstu =  text
        self.kolor_zaznaczenia = selection

    def set_fontsize(self,font_size):
        self.rozmiar_fontu = font_size

    def set_font(self, path):
        self.font_path = path

    def get_position(self):
        return self.pozycja_zaznaczenia

    def init(self, lista, dest_surface):
        self.lista = lista
        self.dest_surface = dest_surface
        self.ilosc_pol = len(self.lista)
        self.stworz_strukture()

    def draw(self,przesun=0):
        if przesun:
            self.pozycja_zaznaczenia += przesun
            if self.pozycja_zaznaczenia == -1:
                self.pozycja_zaznaczenia = self.ilosc_pol - 1
            self.pozycja_zaznaczenia %= self.ilosc_pol
        menu = pygame.Surface((self.menu_width, self.menu_height))
        menu.fill(self.kolor_tla)
        zaznaczenie_rect = self.pola[self.pozycja_zaznaczenia].zaznaczenie_rect
        pygame.draw.rect(menu,self.kolor_zaznaczenia,zaznaczenie_rect)

        for i in xrange(self.ilosc_pol):
            menu.blit(self.pola[i].pole,self.pola[i].pole_rect)
        self.dest_surface.blit(menu,self.pozycja_wklejenia)
        return self.pozycja_zaznaczenia

    def stworz_strukture(self):
        przesuniecie = 0
        self.menu_height = 0
        self.font = pygame.font.Font(self.font_path, self.rozmiar_fontu)
        for i in xrange(self.ilosc_pol):
            self.pola.append(self.Pole())
            self.pola[i].tekst = self.lista[i]
            self.pola[i].pole = self.font.render(self.pola[i].tekst, 1, self.kolor_tekstu)

            self.pola[i].pole_rect = self.pola[i].pole.get_rect()
            przesuniecie = int(self.rozmiar_fontu * 0.2)

            height = self.pola[i].pole_rect.height
            self.pola[i].pole_rect.left = przesuniecie
            self.pola[i].pole_rect.top = przesuniecie+(przesuniecie*2+height)*i

            width = self.pola[i].pole_rect.width+przesuniecie*2
            height = self.pola[i].pole_rect.height+przesuniecie*2
            left = self.pola[i].pole_rect.left-przesuniecie
            top = self.pola[i].pole_rect.top-przesuniecie

            self.pola[i].zaznaczenie_rect = (left,top ,width, height)
            if width > self.menu_width:
                    self.menu_width = width
            self.menu_height += height
        x = self.dest_surface.get_rect().centerx - self.menu_width / 2
        y = self.dest_surface.get_rect().centery - self.menu_height / 2
        mx, my = self.pozycja_wklejenia
        self.pozycja_wklejenia = (x+mx, y+my)
