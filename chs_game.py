import tkinter as tk
from chs_board import Board
from PIL import Image, ImageTk
import numpy as np


class Game(tk.Canvas):
    def __init__(self, master, theme=("#D2B48C", "#664229", "#B5D3E7")):
        super().__init__(master, width=800, height=800)

        self.bind("<Button-1>", self.handle_move)

        self.grid(row=0, column=1, rowspan=8)

        self.board = Board()
        self.rects = np.empty((8, 8), dtype=np.object)

        self.images = set()

        self.theme = theme

        self.draw_board()
        self.reset_board()

        self.clicked = False
        self.selected = None
        self.allowed = set()
        self.captured = {1: [], -1: []}

        self.turn = 1

    def draw_board(self):
        x = 0
        for i in range(8):
            y = 0
            for j in range(8):
                rect = self.create_rectangle(
                    x, y, x + 100, y + 100, fill=self.theme[(i + j) % 2], width=0.5,
                )
                self.rects[j][i] = rect
                y += 100
            x += 100

    def cls_board(self):
        for i in range(8):
            for j in range(8):
                pce = self.board[i][j]
                if pce.color != 0:
                    self.rmv_piece(pce)

    def reset_board(self):
        self.board.setup()
        self.cls_board()

        for row in (0, 1, 6, 7):
            for col in range(8):
                self.put_piece(self.board[row][col])

    def handle_move(self, event):
        loc = (event.y // 100, event.x // 100)
        slot = self.board[loc]

        if not self.clicked:
            if slot.color == self.turn:
                self.do_select(loc, slot)
            elif slot.color == 0:
                print("Empty location!")
            else:
                print("Select own piece")

        else:
            if loc in self.allowed:
                self.do_move(loc, slot)
            elif slot.color == self.turn:
                self.clicked = False
                self.handle_move(event)
            else:
                print("Invalid move")

    def do_select(self, loc, slot):
        self.selected = slot

        self.reset_allowed()
        self.allowed = slot.getMoves(self.board)
        self.draw_allowed()

        self.clicked = True

    def do_move(self, loc, slot):
        if slot.color != 0:
            self.rmv_piece(slot)
            self.captured[self.turn].append(slot)

        self.rmv_piece(self.selected)
        self.board.move(self.selected.coord, loc)
        self.put_piece(self.selected)

        self.reset_allowed()

        if self.selected.type == "Pawn" or self.selected.type == "King":
            self.selected.updateMoved(True)

        self.clicked = False
        self.turn *= -1
        self.selected = None

    def put_piece(self, piece):
        row, col = piece.coord

        IMGSIZE = 80

        img = ImageTk.PhotoImage(image=piece.image)
        self.images.add(img)

        self.create_image(
            (col * 100 + 50, row * 100 + 50), image=img, anchor=tk.CENTER,
        )

    def rmv_piece(self, piece):
        row, col = piece.coord
        rPoint, cPoint = row * 100, col * 100

        newRect = self.create_rectangle(
            cPoint,
            rPoint,
            cPoint + 100,
            rPoint + 100,
            fill=self.theme[(row + col) % 2],
            width=0.5,
        )
        self.rects[row][col] = newRect

    def draw_allowed(self):
        allowed = self.allowed
        print(allowed)
        if (len(allowed)) > 0:
            for row, col in allowed:
                self.itemconfig(self.rects[row][col], fill=self.theme[2])
        else:
            print("No legal moves for selected piece")

    def reset_allowed(self):
        for row, col in self.allowed:
            self.itemconfig(self.rects[row][col], fill=self.theme[(row + col) % 2])


if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()
