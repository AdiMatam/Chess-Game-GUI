import tkinter as tk
import numpy as np
from chsPieces import *
from PIL import Image, ImageTk


class Game(tk.Canvas):
    def __init__(self, master, theme=("#D2B48C", "#664229", "#B5D3E7")):
        super().__init__(master, width=800, height=800)

        self.bind("<Button-1>", self.handleMove)
        self.grid(row=0, column=1, rowspan=8)

        self.board = np.empty((8, 8), dtype=np.object)

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
                self.create_rectangle(
                    x,
                    y,
                    x + 100,
                    y + 100,
                    outline="white",
                    fill=self.theme[(i + j) % 2],
                    tags=f"{j},{i}",
                )
                y += 100
            x += 100

    def resetBoard(self):
        """TODO: CLEAR PIECES ON CANVAS"""

        for idx in range(8):
            blk = (1, idx)
            self.board[blk] = Pawn(-1, blk)
            self.drawPiece(self.board[blk])

            wht = (6, idx)
            self.board[wht] = Pawn(1, wht)
            self.drawPiece(self.board[wht])

        row = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

        for idx, Item in enumerate(row):
            blk = (0, idx)
            self.board[blk] = Item(-1, blk)
            self.drawPiece(self.board[blk])

            wht = (7, idx)
            self.board[wht] = Item(1, wht)
            self.drawPiece(self.board[wht])

        for i in range(2, 6):
            for j in range(8):
                self.board[i][j] = Empty(0)

    def handleMove(self, event):
        selected = self.board[event.y // 100][event.x // 100]
        if not self.clicked:
            if selected.color == self.turn:
                print(f"Selected {selected.type} at {selected.coord}")
                self.selected = selected

                self.resetAllowed()
                self.allowed = selected.getMoves(self.board)
                self.drawAllowed()

                self.clicked = True

            elif selected.color == self.turn * -1:
                print("Select own piece")

            elif selected.color == 0:
                print("No piece at this location")
        else:
            newPos = (event.y // 100, event.x // 100)
            slot = self.board[newPos]
            if newPos in self.allowed:
                if slot.color == self.turn * -1:
                    self.captured[self.turn].append(slot.type)
                    print(self.captured)
                    self.delPiece(slot)

                self.execMove(newPos)
                self.isCheck()

                if self.selected.type == "pawn" or self.selected.type == "king":
                    self.selected.updateMoved(True)

                self.selected = None
                self.clicked = False

                self.resetAllowed()

                self.turn *= -1

            elif slot.color == self.turn:
                self.clicked = False
                self.handleMove(event)

            else:
                print("Invalid Move")

    def execMove(self, newPos):
        self.delPiece(self.selected)
        self.board[self.selected.coord] = Empty(0)

        self.selected.updatePos(newPos)

        self.drawPiece(self.selected)
        self.board[newPos] = self.selected

    def isCheck(self):
        kingPos = None
        myPieces = set()
        for i in range(8):
            for j in range(8):
                if (
                    type(self.board[i][j]) is King
                    and self.board[i][j].color == self.turn * -1
                ):
                    kingPos = self.board[i][j].coord
                elif self.board[i][j].color == self.turn:
                    myPieces.add(self.board[i][j])

        for pce in myPieces:
            if kingPos in pce.getMoves(self.board):
                print("checked")

    def drawPiece(self, piece):
        row, col = piece.coord

        opened = Image.open(piece.image).resize((90, 90), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(image=opened)
        self.images.add(img)

        self.create_image(
            (col * 100 + 50, row * 100 + 50),
            image=img,
            anchor="c",
            tags=f"{row},{col}img",
        )

    def delPiece(self, piece):
        row, col = piece.coord
        self.delete(f"{row},{col}img")

    def drawAllowed(self):
        allowed = self.allowed
        print(allowed)

        if (len(allowed)) > 0:
            for row, col in allowed:
                self.itemconfig(f"{row},{col}", fill=self.theme[2])
        else:
            print("No legal moves for selected piece")

    def resetAllowed(self):
        if len(self.allowed) > 0:
            for row, col in self.allowed:
                self.itemconfig(f"{row},{col}", fill=self.theme[(row + col) % 2])


if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()
