# The file that constants the constants for the program. (For consistency)
from collections import defaultdict

EMP = 0
BLK = 1
WHT = 2

BLACK = (0, 0, 0)
WHITE = (255,255,255)
GREEN = ( 75,166, 50)
BLUE = (50,75,166)
BG = (90,200,80)
YELLOW = (240,220,0)
GREY = (51,51,51)
DULLYELLOW =  (255, 255, 153)
LIGHTBLUE = (153,102,255)
tileMap = defaultdict()
tileMap[BLK] = 0
tileMap[WHT] = 1


HUGE = 10000000