import os
import pygame
from pygame.image import load

from const import *
from client import Client
from board import Board


class Game(Board, Client):
    def __init__(self, win, theme="traditional"):
        Board.__init__(self)
        Client.__init__(self)
        self.win = win
        self.theme = theme

        self.images = {}
        self.store_images()
        self.draw_board()
        self.setup_board()

        self.clicked = False

    def store_images(self):
        for file in os.listdir("images"):
            key = file[: file.index(".")]
            self.images[key] = load(rf"images\{file}")

    def square(self, x, y, size=BOX, color=None):
        x, y = int(x), int(y)
        if color:
            pygame.draw.rect(self.win, color, (x, y, size, size))
        else:
            row, col = to_rowcol(x, y)
            pygame.draw.rect(self.win, self.theme[(row + col) % 2], (x, y, size, size))

    def draw_board(self):
        for x in range(0, 800, 100):
            for y in range(0, 800, 100):
                self.square(x, y)

    def setup_board(self):
        for row in range(8):
            for col in range(8):
                if self.has_piece(row, col):
                    pce = self.piece_at(row, col)
                    self.draw_piece(pce, *to_xy(*pce.coord))

    def draw_piece(self, piece, x, y):
        offset = (BOX - IMGSIZE) // 2
        self.win.blit(self.images.get(piece.image), (int(x + offset), int(y + offset)))

    def draw_allowed(self):
        for row, col in self.allowed:
            x, y = to_xy(row, col)
            cx, cy = x + HFBOX, y + HFBOX
            if self.has_piece(row, col):
                self.square(x, y, color=self.theme[2])
                pygame.draw.circle(self.win, self.theme[(row + col) % 2], (cx, cy), 85)
                self.draw_piece(self.selected, x, y)
            else:
                pygame.draw.circle(self.win, self.theme[2], (cx, cy), 30)

    def reset_allowed(self):
        for row, col in self.allowed:
            self.square(*to_xy(row, col))

