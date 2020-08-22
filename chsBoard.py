import numpy as np
from chsPieces import Rook, Knight, Bishop, Queen, King, Empty, Pawn


class Board:
    def __init__(self):
        self.board = np.empty((8, 8), dtype=np.object)

    def setup(self):
        for idx in range(8):
            self[1][idx] = Pawn(-1, (1, idx))
            self[6][idx] = Pawn(1, (6, idx))

        row = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

        for idx, Item in enumerate(row):
            self[0][idx] = Item(-1, (0, idx))
            self[7][idx] = Item(1, (7, idx))

        for i in range(2, 6):
            for j in range(8):
                self.board[i][j] = Empty(0)

    def move(self, oldPos, newPos):
        self[newPos] = self[oldPos]
        self[oldPos] = Empty(0)
        self[newPos].updatePos(newPos)

    def __getitem__(self, idx):
        return self.board[idx]

    def __setitem__(self, idx, value):
        self.board[idx] = value

    def __repr__(self):
        return f"{self.__module__}{type(self).__name__} object at {hex(id(self))}"

    def __str__(self):
        return np.array2string(self.board)


if __name__ == "__main__":
    b = Board()
    b.setup()
