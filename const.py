from pygame import color


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


def to_rowcol(x, y, player=1):
    row = int(y // BOX) if player == 1 else 7 - int(y // BOX)
    return (row, int(x // BOX))


def to_xy(row, col, player=1):
    if player == -1:
        row = 7 - row
    return (int(col * BOX), int(row * BOX))


# def reflect(row, col):
#     return (abs(7 - row), col)


# def null(row, col):
#     return (row, col)

