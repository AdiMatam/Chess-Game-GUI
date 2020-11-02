import os
import platform
from tkinter.constants import BOTH
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN
from tkinter import Frame, Tk, TclError

from const import *
from themes import ThemeMap
from client import Client


class Game(Client):
    def __init__(self, root, theme="traditional"):
        super().__init__()
        self.connect()
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
        self.board = self.send("get")

        self.store_images()
        self.draw_board()
        self.setup_board()

    def store_images(self):
        for file in os.listdir("images"):
            key = file[: file.index(".")]
            self.images[key] = pygame.image.load(rf"images\{file}")

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
                if self.board.has_piece(row, col):
                    pce = self.board.piece_at(row, col)
                    self.draw_piece(pce, *to_xy(*pce.coord))

    def draw_piece(self, piece, x, y):
        offset = (BOX - IMGSIZE) // 2
        self.win.blit(self.images.get(piece.image), (int(x + offset), int(y + offset)))

    def draw_allowed(self):
        for row, col in self.board.allowed:
            x, y = to_xy(row, col)
            cx, cy = x + HFBOX, y + HFBOX
            if self.board.has_piece(row, col):
                self.square(x, y, color=self.theme[2])
                pygame.draw.circle(self.win, self.theme[(row + col) % 2], (cx, cy), 85)
                self.draw_piece(self.board.selected, x, y)
            else:
                pygame.draw.circle(self.win, self.theme[2], (cx, cy), 30)

    def reset_allowed(self):
        for row, col in self.board.allowed:
            self.square(*to_xy(row, col))

    def update_square(self, row, col):
        x, y = to_xy(row, col)
        self.square(x, y)
        if self.board.has_piece(row, col):
            self.draw_piece(self.board.piece_at(row, col), x, y)

    def RUN(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == QUIT:
                    run = False
                elif event.type == MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    row, col = to_rowcol(*mouse)
                    self.board = self.send("get")
                    if self.board.selected is None or self.board.is_mine(row, col):
                        self.reset_allowed()
                        self.board = self.send(f"select,{row},{col}")
                        self.draw_allowed()
                    else:
                        self.board = self.send(f"move,{row},{col}")
                        self.reset_allowed()
            if self.board.selected is None:
                for coord in self.board.updateSquares:
                    self.update_square(*coord)
                self.board = self.send(f"update,{self.id}")
            if self.board.is_updated():
                self.board.clear_went()
                self.board.updateSquares.clear()
            pygame.display.update()
            try:
                self.root.update()
            except TclError:
                run = False
        pygame.quit()


try:
    root = Tk()
    root.resizable(False, False)
    root.title("Chess")
    game = Game(root)
    root.update_idletasks()
    game.RUN()
except Exception as e:
    print(e)
finally:
    pygame.quit()
