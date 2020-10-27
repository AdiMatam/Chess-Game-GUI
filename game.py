import os
import platform
from tkinter.constants import BOTH
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN
from pygame.image import load
from tkinter import Frame, Tk, TclError

from const import *
from client import Client
from themes import ThemeMap


class Game:
    def __init__(self, root, theme="traditional"):
        # super().__init__()
        # self.connect()
        self.root = root

        self.gameFrame = Frame(root, width=800, height=800)
        self.gameFrame.pack(fill=BOTH)
        os.environ["SDL_WINDOWID"] = str(self.gameFrame.winfo_id())
        if platform.system == "Windows":
            os.environ["SDL_VIDEODRIVER"] = "windib"

        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.theme = ThemeMap.get(theme)

        self.images = {}
        self.store_images()
        self.draw_board()
        # self.setup_board()

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

    # def setup_board(self):
    #     board = self.get_board()
    #     for row in range(8):
    #         for col in range(8):
    #             if board.has_piece(row, col):
    #                 pce = board.piece_at(row, col)
    #                 self.draw_piece(pce, *to_xy(*pce.coord))

    # def draw_piece(self, piece, x, y):
    #     offset = (BOX - IMGSIZE) // 2
    #     self.win.blit(self.images.get(piece.image), (int(x + offset), int(y + offset)))

    # def draw_allowed(self):
    #     board = self.get_board()
    #     for row, col in board.allowed:
    #         x, y = to_xy(row, col)
    #         cx, cy = x + HFBOX, y + HFBOX
    #         if board.has_piece(row, col):
    #             self.square(x, y, color=self.theme[2])
    #             pygame.draw.circle(self.win, self.theme[(row + col) % 2], (cx, cy), 85)
    #             self.draw_piece(board.selected, x, y)
    #         else:
    #             pygame.draw.circle(self.win, self.theme[2], (cx, cy), 30)

    # def reset_allowed(self):
    #     for row, col in self.get_board():
    #         self.square(*to_xy(row, col))

    def RUN(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == QUIT:
                    run = False
                elif event.type == MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    # self.reset_allowed()
                    # bo = self.get_board()
                    # if not self.clicked:
                    #     self.send("select")
                    #     bo.set_selected(bo.piece_at(*to_rowcol(*mouse)))
                    #     bo.store_allowed()
                    # else:
                    #     pass
            pygame.display.update()
            try:
                self.root.update()
            except TclError:
                run = False
        pygame.quit()


try:
    root = Tk()
    root.resizable(False, False)
    game = Game(root)
    root.update_idletasks()
    game.RUN()
except Exception as e:
    print(e)
finally:
    pygame.quit()
