import pygame


# Class was found online.
# http://www.pygame.org/project-menu_key-2278-.html
# Quite possibly another natural language
class Menu:
    menuList = []
    field = []
    fontSize = 32
    font_path = 'font/coders_crux.ttf'
    font = pygame.font.Font
    dest_surface = pygame.Surface
    ilosc_pol = 0
    bgColor = (51,51,51)
    textColor =  (255, 255, 153)
    selectColor = (153,102,255)
    itemSelect = 0
    pastePosition = (0,0)
    menu_width = 0
    menu_height = 0

    class Pole:
        text = ''
        pole = pygame.Surface
        pole_rect = pygame.Rect
        selectedRect = pygame.Rect

    def move_menu(self, top, left):
        self.pastePosition = (top,left)

    def set_colors(self, text, selection, background):
        self.bgColor = background
        self.textColor = text
        self.selectColor = selection

    def set_fontsize(self,font_size):
        self.fontSize = font_size

    def set_font(self, path):
        self.font_path = path

    def get_position(self):
        return self.itemSelect

    def init(self, lista, dest_surface):
        self.menuList = lista
        self.dest_surface = dest_surface
        self.ilosc_pol = len(self.menuList)
        self.createStructure()

    def draw(self , move=0):
        if move:
            self.itemSelect += move
            if self.itemSelect == -1:
                self.itemSelect = self.ilosc_pol - 1
            self.itemSelect %= self.ilosc_pol
        menu = pygame.Surface((self.menu_width, self.menu_height))
        menu.fill(self.bgColor)
        selectedRect = self.field[self.itemSelect].zaznaczenie_rect
        pygame.draw.rect(menu,self.selectColor,selectedRect)

        for i in xrange(self.ilosc_pol):
            menu.blit(self.field[i].pole,self.field[i].pole_rect)
        self.dest_surface.blit(menu, self.pastePosition)
        return self.itemSelect

    def createStructure(self):
        offset = 0
        self.menu_height = 0
        self.font = pygame.font.Font(self.font_path, self.fontSize)
        for i in xrange(self.ilosc_pol):
            self.field.append(self.Pole())
            self.field[i].tekst = self.menuList[i]
            self.field[i].pole = self.font.render(self.field[i].tekst, 1, self.textColor)

            self.field[i].pole_rect = self.field[i].pole.get_rect()
            offset = int(self.fontSize * 0.2)

            height = self.field[i].pole_rect.height
            self.field[i].pole_rect.left = offset
            self.field[i].pole_rect.top = offset+(offset*2+height)*i

            width = self.field[i].pole_rect.width+offset*2
            height = self.field[i].pole_rect.height+offset*2
            left = self.field[i].pole_rect.left-offset
            top = self.field[i].pole_rect.top-offset

            self.field[i].zaznaczenie_rect = (left,top ,width, height)
            if width > self.menu_width:
                    self.menu_width = width
            self.menu_height += height
        x = self.dest_surface.get_rect().centerx - self.menu_width / 2
        y = self.dest_surface.get_rect().centery - self.menu_height / 2
        mx, my = self.pastePosition
        self.pastePosition = (x+mx, y+my)
