import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN

from chs_board import Board
from chs_themes import themes
from chs_const import *


class Game(Board):
    def __init__(self, window, theme="Traditional", first="WHITE"):
        super().__init__()
        self.window = window

        self.theme = themes.get(theme.lower())

        self.reset_board()
        self.clicked = False

    def square(self, x, y, size, color=None):
        if color:
            return pygame.draw.rect(self.window, color, (int(x), int(y), size, size))
        else:
            rowcol = int(sum(self.to_rowcol(x, y)))
            return pygame.draw.rect(
                self.window, self.theme[rowcol % 2], (int(x), int(y), size, size)
            )

    def draw_board(self):
        for x in range(0, WIDTH, BOX):
            for y in range(0, HEIGHT, BOX):
                self.square(x, y, BOX)

    def reset_board(self):
        self.draw_board()
        self.setup()

        for row in (0, 1, 6, 7):
            for col in range(8):
                pce = self.piece_at(row, col)
                self.draw_piece(pce, *self.to_xy(*pce.coord))

    def draw_piece(self, piece, x, y):
        offset = (BOX - IMGSIZE) // 2
        self.window.blit(piece.image, (int(x + offset), int(y + offset)))

    def cover_piece(self, piece):
        self.square(*self.to_xy(*piece.coord), BOX)

    def select_piece(self, x, y):
        row, col = self.to_rowcol(x, y)
        if self.has_piece(row, col) and self.is_mine(row, col):
            self.set_selected(self.piece_at(row, col))
            self.hilite_selected(*self.to_xy(row, col))

            self.reset_allowed()
            self.store_allowed()
            self.draw_allowed()

            self.clicked = True

        else:
            print("Invalid Selection")

    def hilite_selected(self, x, y):
        self.square(x, y, BOX, self.theme[2])
        circColor = self.theme[sum(self.to_rowcol(x, y)) % 2]
        pygame.draw.circle(self.window, circColor, (x + HFBOX, y + HFBOX), RADIUS)
        self.draw_piece(self.selected, x, y)

    def move_piece(self, x, y):
        self.reset_allowed()
        row, col = self.to_rowcol(x, y)
        pce = self.piece_at(row, col)

        if (row, col) in self.allowed:
            self.draw_along_path(
                self.selected, self.to_xy(*self.selected.coord), self.to_xy(row, col)
            )
            if pce.color != 0:
                self.cover_piece(pce)
                self.draw_piece(self.selected, *self.to_xy(row, col))
                self.captured.get(self.turn).append(pce)

            self.move(self.selected.coord, (row, col))

            if self.selected.type == "Pawn" or self.selected.type == "King":
                self.selected.updateMoved(True)

            self.switch_turn()
            self.clicked = False

        elif pce.color == self.turn:
            self.cover_piece(self.selected)
            self.draw_piece(self.selected, *self.to_xy(*self.selected.coord))
            self.select_piece(x, y)

        else:
            print("Invalid selection")

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
            abslope = abs(ydiff / xdiff)

        scale = max(1, self.get_distance(xdiff, ydiff) // 200)
        while abs(x1 - x2) >= 2 or abs(y1 - y2) >= 2:
            x1 += dirx * scale
            y1 += diry * abslope * scale
            mainRect = self.redraw_neighbors(x1, y1)
            self.draw_piece(piece, x1, y1)
            pygame.display.update(mainRect)
            pygame.time.delay(2)

    @staticmethod
    def get_distance(dx, dy):
        dist = (dx ** 2 + dy ** 2) ** (1 / 2)
        return abs(dist)

    def redraw_neighbors(self, x, y):
        row, col = self.to_rowcol(x, y)

        rects = []
        nx = ny = 0
        for rShift in (-1, 0, 1):
            for cShift in (-1, 0, 1):
                nRow = int(row + rShift)
                nCol = int(col + cShift)
                if 0 <= nRow <= 7 and 0 <= nCol <= 7:
                    nx, ny = self.to_xy(nRow, nCol)
                    rects.append(self.square(nx, ny, BOX))
                    if self.has_piece(nRow, nCol) and self.selected.coord != (nRow, nCol):
                        self.draw_piece(self.piece_at(nRow, nCol), nx, ny)

        return pygame.Rect(nx, ny, BOX, BOX).unionall(rects)

    def draw_allowed(self):
        shrink = 10
        if len(self.allowed) > 0:
            for row, col in self.allowed:
                x, y = self.to_xy(row, col)
                self.square(x + shrink, y + shrink, BOX - shrink * 2, self.theme[2])
                if self.has_piece(row, col):
                    self.draw_piece(self.piece_at(row, col), x, y)
        else:
            print("No legal moves for selected piece")

    def reset_allowed(self):
        for row, col in self.allowed:
            x, y = self.to_xy(row, col)
            self.square(x, y, BOX)
            if self.has_piece(row, col):
                self.draw_piece(self.piece_at(row, col), x, y)

    @staticmethod
    def to_rowcol(x, y):
        return (y // BOX, x // BOX)

    @staticmethod
    def to_xy(row, col):
        return (col * BOX, row * BOX)


pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))

game = Game(win)
pygame.display.update()

run = True

# MAINLOOP
while run:
    update = False
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            update = True
            if not game.clicked:
                game.select_piece(*mouse)
            else:
                game.move_piece(*mouse)

    if update:
        pygame.display.update()


pygame.quit()
