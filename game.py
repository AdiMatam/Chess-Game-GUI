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

        # self.func = null if self.id == 1 else reflect

        self.root = root
        root.title(f"Player {self.id}")
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
        self.setup_board()

    def store_images(self):
        for file in os.listdir("images"):
            key = file[: file.index(".")]
            self.images[key] = pygame.image.load(rf"images\{file}")

    def square(self, x, y, size=BOX, color=None):
        x, y = int(x), int(y)
        if color:
            return pygame.draw.rect(self.win, color, (x, y, size, size))
        else:
            row, col = to_rowcol(x, y)
            return pygame.draw.rect(self.win, self.theme[(row + col) % 2], (x, y, size, size))

    def setup_board(self):
        for row in range(8):
            for col in range(8):
                self.update_square(row, col)

    def draw_piece(self, piece, x, y):
        offset = (BOX - IMGSIZE) // 2
        self.win.blit(self.images.get(piece.image), (int(x + offset), int(y + offset)))

    def draw_allowed(self):
        for row, col in self.board.allowed:
            x, y = to_xy(row, col)
            cx, cy = x + HFBOX, y + HFBOX
            if self.board.has_piece(row, col):
                self.square(x, y, color=self.theme[2])
                pygame.draw.circle(self.win, self.theme[(row + col) % 2], (cx, cy), RADIUS)
                self.draw_piece(self.board.piece_at(row, col), x, y)
            else:
                pygame.draw.circle(self.win, self.theme[2], (cx, cy), 30)

    def reset_allowed(self):
        for row, col in self.board.allowed:
            self.update_square(row, col)

    def update_square(self, row, col):
        x, y = to_xy(row, col)
        self.square(x, y)
        if self.board.has_piece(row, col):
            self.draw_piece(self.board.piece_at(row, col), x, y)

    def draw_along_path(self, piece, fro: tuple, to: tuple):
        x1, y1 = to_xy(*fro)
        x2, y2 = to_xy(*to)

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
            mainRect = self.redraw_neighbors(x1, y1, to)
            self.draw_piece(piece, x1, y1)
            pygame.display.update(mainRect)
            pygame.time.delay(2)

    def redraw_neighbors(self, x, y, dest: tuple):
        row, col = to_rowcol(x, y)
        rects = []
        nx = ny = 0
        for rShift in (-1, 0, 1):
            for cShift in (-1, 0, 1):
                nRow = int(row + rShift)
                nCol = int(col + cShift)
                if 0 <= nRow <= 7 and 0 <= nCol <= 7:
                    nx, ny = to_xy(nRow, nCol)
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
                    row, col = to_rowcol(*mouse)
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
    root.title("Chess")
    game = Game(root)
    root.update_idletasks()
    game()
except Exception as e:
    print(e)
finally:
    pygame.quit()
