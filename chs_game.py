import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN
from pygame.image import load

from chs_const import *
from chs_net import Network

net = Network()
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
theme = ((210, 180, 140), (102, 66, 41))


def to_rowcol(x, y):
    return (y // BOX, x // BOX)


def to_xy(row, col):
    return (col * BOX, row * BOX)


def update():
    pygame.display.update()


def draw_piece(win, piece, x, y):
    offset = (BOX - IMGSIZE) // 2
    win.blit(load(piece.image), (int(x + offset), int(y + offset)))


def redraw_window(board):
    global win, net, theme
    for row in range(8):
        for col in range(8):
            x, y = to_xy(row, col)
            rect = (x, y, BOX, BOX)
            pygame.draw.rect(win, theme[(row + col) % 2], rect)
            if board.has_piece(row, col):
                draw_piece(win, board.piece_at(row, col), x, y)
    update()


def encode_pos(tup1, tup2):
    return f"{tup1[0]}{tup1[1]}{tup2[0]}{tup2[1]}"


bo = net.send("setup")
redraw_window(bo)

run = True
clicked = False
pos = None

# MAINLOOP
while run:
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == MOUSEBUTTONDOWN:
            if not clicked:
                pos = to_rowcol(*pygame.mouse.get_pos())
            else:
                strpos = encode_pos(pos, to_rowcol(*pygame.mouse.get_pos()))
                net.send(strpos)
            clicked = not clicked

    redraw_window(net.send("get"))


pygame.quit()
