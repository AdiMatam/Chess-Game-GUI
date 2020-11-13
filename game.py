import os
from tkinter import Button, Frame, TclError, Tk

import pygame
from pygame.locals import MOUSEBUTTONDOWN, QUIT

from client import Client
from const import *
from logger import Logger
from themes import ThemeMap
from resizer import resize


class Game(Client):
    def __init__(self, root, theme="traditional"):
        super().__init__()
        self.connect()
        self.root = root
        self.view = self.id

        if self.id == 1:
            self.logger = Logger(r"logs\whitelog.txt")
            self.root.title("WHITE PLAYER")
        else:
            self.logger = Logger(r"logs\blacklog.txt")
            self.root.title("BLACK PLAYER")

        self.setup_tk()

        os.environ["SDL_WINDOWID"] = str(self.gameFrame.winfo_id())
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.theme = ThemeMap.get(theme)

        self.board = self.send("get")

        self.images = {}
        resize()
        for file in os.listdir("images"):
            key = file[: file.index(".")]
            self.images[key] = pygame.image.load(rf"images\{file}")

        self.setup_board()

    def setup_tk(self):
        self.gameFrame = Frame(self.root, width=WIDTH, height=HEIGHT)
        self.gameFrame.grid(row=0, column=0, columnspan=8, rowspan=8)
        self.flipButton = Button(
            self.root, text="Flip", bg="white", font=FONT(BUTFNT), command=self.flip,
        )
        self.flipButton.grid(row=8, column=0, columnspan=8, sticky="we")

    def flip(self):
        self.view *= -1
        self.setup_board()

    def square(self, x, y, size=BOX, color=None):
        x, y = int(x), int(y)
        if color:
            return pygame.draw.rect(self.win, color, (x, y, size, size))
        else:
            comb = sum(to_rowcol(x, y))
            return pygame.draw.rect(self.win, self.theme[comb % 2], (x, y, size, size))

    def update_square(self, row, col):
        x, y = to_xy(row, col, self.view)
        self.square(x, y)
        if self.board.has_piece(row, col):
            self.draw_piece(self.board.piece_at(row, col), x, y)

    def setup_board(self):
        for row in range(8):
            for col in range(8):
                self.update_square(row, col)

    def draw_piece(self, piece, x, y):
        offset = (BOX - IMGSIZE) // 2
        self.win.blit(self.images.get(piece.image), (int(x + offset), int(y + offset)))

    def draw_allowed(self):
        for row, col in self.board.allowed:
            x, y = to_xy(row, col, self.view)
            cx, cy = x + HFBOX, y + HFBOX
            if self.board.has_piece(row, col):
                self.square(x, y, color=self.theme[2])
                pygame.draw.circle(self.win, self.theme[(row + col) % 2], (cx, cy), RADIUS)
                self.draw_piece(self.board.piece_at(row, col), x, y)
            else:
                pygame.draw.circle(self.win, self.theme[2], (cx, cy), int(HFBOX * 0.6))

    def reset_allowed(self):
        for row, col in self.board.allowed:
            self.update_square(row, col)

    def draw_along_path(self, piece, fro: tuple, to: tuple):
        x1, y1 = to_xy(*fro, self.view)
        x2, y2 = to_xy(*to, self.view)

        xdiff = x2 - x1
        ydiff = y2 - y1

        dirx = (xdiff) / max(1, abs(xdiff))
        diry = (ydiff) / max(1, abs(ydiff))

        abslope = 1 if xdiff == 0 else abs(ydiff / xdiff)

        scale = max(1, self.get_distance(xdiff, ydiff) // (BOX * 2))
        while abs(x1 - x2) >= 2 or abs(y1 - y2) >= 2:
            x1 += dirx * scale
            y1 += diry * abslope * scale
            mainRect = self.redraw_neighbors(x1, y1, to)
            self.draw_piece(piece, x1, y1)
            pygame.display.update(mainRect)
            pygame.time.delay(2)

    def redraw_neighbors(self, x, y, dest: tuple):
        row, col = to_rowcol(x, y, self.view)
        rects = []
        nx = ny = 0
        for rShift in (-1, 0, 1):
            for cShift in (-1, 0, 1):
                nRow = int(row + rShift)
                nCol = int(col + cShift)
                if 0 <= nRow <= 7 and 0 <= nCol <= 7:
                    nx, ny = to_xy(nRow, nCol, self.view)
                    rects.append(self.square(nx, ny, BOX))
                    if self.board.has_piece(nRow, nCol) and dest != (nRow, nCol):
                        self.draw_piece(self.board.piece_at(nRow, nCol), nx, ny)

        return pygame.Rect(x, y, BOX, BOX).unionall(rects)

    @staticmethod
    def get_distance(dx, dy):
        dist = (dx ** 2 + dy ** 2) ** (1 / 2)
        return abs(dist)

    def __call__(self):
        run = True
        while run:
            self.board = self.send("get")
            for event in pygame.event.get():
                if event.type == QUIT:
                    run = False
                elif event.type == MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    row, col = to_rowcol(mouse[0], mouse[1], self.view)
                    if self.board.turn != self.id:
                        break
                    if self.board.is_mine(row, col):
                        self.reset_allowed()
                        self.board = self.send(f"select,{row},{col}")
                        self.draw_allowed()
                    else:
                        self.board = self.send(f"move,{row},{col}")
                        if self.board.moved:
                            self.reset_allowed()
            if self.board.moved and self.board.pending_update(self.id):
                self.draw_along_path(self.board.selected, self.board.start, self.board.dest)
                self.board = self.send(f"updated,{self.id}")
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
    game()
    game.logger.close()
except Exception as e:
    print(e)
finally:
    pygame.quit()
