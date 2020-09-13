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

        self.selected = None
        self.allowed = set()
        self.captured = {1: [], -1: []}
        self.update_set = set()

    def draw_board(self):
        x = 0
        for col in range(8):
            y = 0
            for row in range(8):
                self.make_rect(self.theme[(row + col) % 2], (x, y, BOX, BOX))
                if self.board.has_piece(row, col):
                    self.draw_piece(self.board[row][col], x + HFBOX, y + HFBOX)
                y += BOX
            x += BOX

    def select_piece(self, x, y):
        row, col = self.to_rowcol(x, y)
        print(row, col)
        if self.board.has_piece(row, col) and self.board[row][col].color == self.turn:
            self.selected = self.board[row][col]
            self.hilite_selected(row, col)

            self.reset_allowed()
            self.allowed = self.selected.get_moves(self.board)
            self.draw_allowed()
            return True

        else:
            print("Invalid Selection")
            return False

    def move_piece(self, x, y):
        rowcol = self.to_rowcol(x, y)
        if rowcol in self.allowed:
            fro = self.to_xy(*self.selected.coord)

            self.animate(fro, (x, y))
            self.board.move(self.selected.coord, rowcol)
            self.reset_allowed()
            self.turn *= 1

            return False

        elif self.board[rowcol].color == self.turn:
            self.select_piece(x, y)
            return False

        else:
            print("Invalid Move")
            return True

    def animate(self, fro: tuple, to: tuple):
        x1, y1 = fro
        x2, y2 = to

        slope = (y2 - y1) / (x2 - x1)
        while True:
            if abs(x2 - x1) < 10 and abs(y2 - y1) < 10:
                return
            x1 += 1
            y1 += slope
            self.draw_piece(self.selected, x1, y1)
            pygame.display.update()

    def reset_allowed(self):
        for row, col in self.allowed:
            x, y = self.to_xy(row, col)
            color = self.theme[(row + col) % 2]
            self.update_set.add(self.make_rect(color, (x, y, BOX, BOX)))

    def draw_allowed(self):
        for row, col in self.allowed:
            x, y = self.to_xy(row, col)
            rX = x + HFBOX - LEGALBOX // 2
            rY = y + HFBOX - LEGALBOX // 2
            self.update_set.add(
                self.make_rect(self.theme[2], (rX, rY, LEGALBOX, LEGALBOX))
            )

    def hilite_selected(self, row, col):
        x, y = self.to_xy(row, col)
        self.update_set.add(self.make_rect(self.theme[2], (x, y, BOX, BOX)))

        circColor = self.theme[(row + col) % 2]
        pygame.draw.circle(self.window, circColor, (x + HFBOX, y + HFBOX), RADIUS)
        self.draw_piece(self.selected, x + HFBOX, y + HFBOX)

    def draw_piece(self, piece, x, y):
        offset = IMGSIZE // 2
        self.window.blit(piece.image, (int(x - offset), int(y - offset)))

    def make_rect(self, color: tuple, rect_params: tuple):
        pygame.draw.rect(self.window, color, rect_params)
        return rect_params

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
game.draw_board()
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
            game.update_set.clear()
            mousePos = pygame.mouse.get_pos()
            if not clicked:
                clicked = game.select_piece(*mousePos)
            else:
                clicked = game.move_piece(*mousePos)

    for rect in game.update_set:
        update_screen(pygame.Rect(rect))
#

pygame.quit()
