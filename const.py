IP = "10.0.0.58"
WIDTH = HEIGHT = 640

### DONT CHANGE BELOW THIS ###

from PIL import Image
import os


ADDR = (IP, 10000)
BUF = 4096

BOX = HEIGHT // 8
HFBOX = BOX // 2
IMGSIZE = HEIGHT // 10
RADIUS = int(HFBOX * 0.96)
BUTFNT = HEIGHT // 50

font = lambda size: ("Calibri", size, "bold")


def to_rowcol(x, y, player=1):
    row = int(y // BOX)
    if player == -1:
        row = 7 - row
    return (row, int(x // BOX))


def to_xy(row, col, player=1):
    if player == -1:
        row = 7 - row
    return (int(col * BOX), int(row * BOX))


def resize():
    img = Image.open(r"images\bbishop.png")
    if img.size[0] == IMGSIZE:
        return
    for file in os.listdir("images"):
        path = fr"images\{file}"
        img = Image.open(path).resize((IMGSIZE, IMGSIZE))
        img.save(path)
