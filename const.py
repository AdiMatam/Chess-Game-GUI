IP = "10.0.0.58"

### DONT CHANGE BELOW THIS ###

ADDR = (IP, 10000)
BUF = 4096


WIDTH = 800
HEIGHT = 800
BOX = HEIGHT // 8
HFBOX = BOX // 2
IMGSIZE = 80
RADIUS = 48

BLACK = (0, 0, 0)


def to_rowcol(x, y):
    return (int(y // BOX), int(x // BOX))


def to_xy(row, col):
    return (int(col * BOX), int(row * BOX))


def reflect(row, col):
    return (abs(7 - row), col)


def null(row, col):
    return (row, col)

