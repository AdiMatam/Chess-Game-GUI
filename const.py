WIDTH = 800
HEIGHT = 800
BOX = HEIGHT // 8
HFBOX = BOX // 2
IMGSIZE = 80
RADIUS = 45

BLACK = (0, 0, 0)

ADDR = ("10.0.0.58", 10000)
BUF = 4096


def to_rowcol(x, y):
    return (int(y // BOX), int(x // BOX))


def to_xy(row, col):
    return (int(col * BOX), int(row * BOX))


def reverse(coord: tuple):
    return (abs(7 - coord[0]), abs(7 - coord[1]))

