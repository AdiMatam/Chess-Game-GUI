import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN

from chs_board import Board
from chs_themes import themes
from chs_const import *
import numpy as np


class Game:
    player = {"WHITE": 1, "BLACK": -1}

    def __init__(self, window, theme="Traditional", first="WHITE"):
        self.window = window
        self.board = Board()
        self.turn = Game.player.get(first.upper())
        self.theme = themes.get(theme.lower())

        self.reset_board()

        self.selected = None
        self.allowed = set()
        self.captured = {1: [], -1: []}

    def square(self, x, y, size, color=None):
        if color:
            pygame.draw.rect(self.window, color, (x, y, size, size))
        else:
            row, col = self.to_rowcol(x, y)
            pygame.draw.rect(
                self.window, self.theme[(int(row) + int(col)) % 2], (int(x), int(y), size, size)
            )

    def draw_board(self):
        for x in range(0, 800, 100):
            for y in range(0, 800, 100):
                self.square(x, y, BOX)

    def reset_board(self):
        self.draw_board()
        self.board.setup()

        for row in (0, 1, 6, 7):
            for col in range(8):
                pce = self.board[row][col]
                self.draw_piece(pce, *self.to_xy(*pce.coord))

    def draw_piece(self, piece, x, y):
        offset = (BOX - IMGSIZE) // 2
        self.window.blit(piece.image, (int(x + offset), int(y + offset)))

    def cover_piece(self, piece):
        self.square(*self.to_xy(*piece.coord), BOX)

    def select_piece(self, x, y):
        row, col = self.to_rowcol(x, y)
        if self.board.has_piece(row, col) and self.board[row][col].color == self.turn:
            self.selected = self.board[row][col]
            # self.hilite_selected(*self.to_xy(row, col))

            self.reset_allowed()
            self.allowed = self.selected.get_moves(self.board)
            self.draw_allowed()
            return True

        else:
            print("Invalid Selection")
            return False

    # def hilite_selected(self, x, y):
    #     self.square(x, y, BOX, self.theme[2])
    #     circColor = self.theme[sum(self.to_rowcol(x, y)) % 2]
    #     pygame.draw.circle(self.window, circColor, (x + HFBOX, y + HFBOX), RADIUS)
    #     self.draw_piece(self.selected, x, y)

    def move_piece(self, x, y):
        self.reset_allowed()
        row, col = self.to_rowcol(x, y)
        pce = self.board[row][col]

        if (row, col) in self.allowed:
            if pce.color != 0:
                self.cover_piece(pce)
                self.captured.get(self.turn).append(pce)

            self.draw_along_path(
                self.selected, self.to_xy(*self.selected.coord), self.to_xy(row, col)
            )
            self.board.move(self.selected.coord, (row, col))

            if self.selected.type == "Pawn" or self.selected.type == "King":
                self.selected.updateMoved(True)

            self.turn *= -1
            return False

        elif pce.color == self.turn:
            self.select_piece(x, y)
        else:
            print("Invalid selection")
            return True

    def draw_along_path(self, piece, fro: tuple, to: tuple):
        x1, y1 = fro
        x2, y2 = to

        xdiff = x2 - x1
        ydiff = y2 - y1

        dirx = (xdiff) / max(1, abs(xdiff))
        diry = (ydiff) / max(1, abs(ydiff))

        if xdiff == 0:
            abslope = 1
        else:
            abslope = abs((ydiff) / (xdiff))

        while x1 != x2 or y1 != y2:
            x1 += dirx
            y1 += diry * abslope
            self.redraw_neighbors(x1, y1)
            self.draw_piece(piece, x1, y1)
            pygame.display.update()
            pygame.time.delay(5)

    def redraw_neighbors(self, x, y):
        row, col = self.to_rowcol(x, y)

        for rShift in (-1, 0, 1):
            for cShift in (-1, 0, 1):
                nRow = row + rShift
                nCol = col + cShift
                if 0 <= nRow <= 7 and 0 <= nCol <= 7:
                    x, y = self.to_xy(nRow, nCol)
                    self.square(x, y, BOX)
                    if self.board.has_piece(nRow, nCol) and self.selected.coord != (nRow, nCol):
                        self.draw_piece(self.board[int(nRow)][int(nCol)], x, y)

    def draw_allowed(self):
        if len(self.allowed) > 0:
            for row, col in self.allowed:
                x, y = self.to_xy(row, col)
                self.square(x, y, BOX, self.theme[2])
                if self.board.has_piece(row, col):
                    self.draw_piece(self.board[row][col], *self.to_xy(row, col))
        else:
            print("No legal moves for selected piece")

    def reset_allowed(self):
        for row, col in self.allowed:
            if not self.board.has_piece(row, col):
                self.square(*self.to_xy(row, col), BOX)

    @staticmethod
    def to_rowcol(x, y):
        return (y // BOX, x // BOX)

    @staticmethod
    def to_xy(row, col):
        return (col * BOX, row * BOX)


def update_screen(rect=None):
    if rect:
        pygame.display.update(rect)
    else:
        pygame.display.update()


pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))

game = Game(win)
update_screen()

# VARS
run = True
clicked = False
#

# MAINLOOP
while run:
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if not clicked:
                clicked = game.select_piece(mx, my)
            else:
                clicked = game.move_piece(mx, my)

    update_screen()
#

pygame.quit()
