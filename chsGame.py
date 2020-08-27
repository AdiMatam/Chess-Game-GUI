import tkinter as tk
from chsBoard import Board
from PIL import Image, ImageTk
import numpy as np


class Game(tk.Canvas):
    def __init__(self, master, theme=("#D2B48C", "#664229", "#B5D3E7")):
        super().__init__(master, width=800, height=800)

        self.bind("<Button-1>", self.handleMove)
        self.grid(row=0, column=1, rowspan=8)

        self.board = Board()
        self.rects = np.empty((8, 8), dtype=np.object)

        self.images = set()

        self.theme = theme

        self.drawBoard()
        self.resetBoard()

        self.clicked = False
        self.selected = None
        self.allowed = set()
        self.captured = {1: [], -1: []}

        self.turn = 1

    def drawBoard(self):
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

    def clsBoard(self):
        for i in range(8):
            for j in range(8):
                pce = self.board[i][j]
                if pce.color != 0:
                    self.delPiece(pce)

    def resetBoard(self):
        self.board.setup()
        self.clsBoard()

        for row in (0, 1, 6, 7):
            for col in range(8):
                self.drawPiece(self.board[row][col])

    def handleMove(self, event):
        loc = (event.y // 100, event.x // 100)
        slot = self.board[event.y // 100][event.x // 100]

        if not self.clicked:
            if slot.color == self.turn:

                self.selected = slot

                self.resetAllowed()
                self.allowed = self.board.filtedMoves(self.turn, *loc)
                self.drawAllowed()

                self.clicked = True

            elif slot.color == 0:
                print("Empty location!")
            else:
                print("Select own piece")

        else:
            if loc in self.allowed:
                if slot.color != 0:
                    self.delPiece(slot)
                    self.captured[self.turn].append(slot)

                self.delPiece(self.selected)
                self.board.move(self.selected.coord, loc)
                self.drawPiece(self.selected)

                self.resetAllowed()

                self.clicked = False
                self.turn *= -1
                self.selected = None

            elif slot.color == self.turn:
                self.clicked = False
                self.handleMove(event)
            else:
                print("Invalid move")

    def drawPiece(self, piece):
        row, col = piece.coord

        IMGSIZE = 80

        opened = Image.open(piece.image).resize((IMGSIZE, IMGSIZE), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(image=opened)
        self.images.add(img)

        self.create_image(
            (col * 100 + 50, row * 100 + 50), image=img, anchor="c",
        )

    def delPiece(self, piece):
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

    def drawAllowed(self):
        allowed = self.allowed
        print(allowed)

        if (len(allowed)) > 0:
            for row, col in allowed:
                self.itemconfig(self.rects[row][col], fill=self.theme[2])
        else:
            print("No legal moves for selected piece")

    def resetAllowed(self):
        for row, col in self.allowed:
            self.itemconfig(self.rects[row][col], fill=self.theme[(row + col) % 2])


def checkKey(event, master):
    if event.char == "q":
        master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.bind("<Key>", lambda e: checkKey(e, root))
    game = Game(root)
    root.mainloop()
