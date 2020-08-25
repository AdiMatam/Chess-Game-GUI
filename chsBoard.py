import numpy as np
from chsPieces import Rook, Knight, Bishop, Queen, King, Empty, Pawn


class Board:
    def __init__(self):
        self.board = np.empty((8, 8), dtype=np.object)
        self.checks = [None, False, False]

    def setup(self):
        for idx in range(8):
            self[1][idx] = Pawn(-1, (1, idx))
            self[6][idx] = Pawn(1, (6, idx))

        row = (Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook)

        for idx, Item in enumerate(row):
            self[0][idx] = Item(-1, (0, idx))
            self[7][idx] = Item(1, (7, idx))

        for i in range(2, 6):
            for j in range(8):
                self.board[i][j] = Empty(0)

    # VOID
    def move(self, oldPos, newPos):
        self[newPos] = self[oldPos]
        self[oldPos] = Empty(0)
        self[newPos].updatePos(newPos)

    # SET <TUPLES>
    def filtedMoves(self, turn, row, col):
        moves = self.board[row][col].getMoves(self.board)
        if self.checks[turn]:
            for move in moves:
                self.board[move] = self.board[row][col]
                self.checkCheck(turn)
                if self.checks[turn]:
                    moves.remove(move)
                self.board[row][col] = self.board[move]

        return moves

    # VOID
    def checkCheck(self, turn):
        king = self.kingPos(turn * -1)
        for pce in self.getPieces(turn):
            allowed = pce.getMoves(self.board)
            if bool(allowed):
                for legal in pce.getMoves(self.board):
                    if legal == king:
                        self.checks[turn] = True
                        return
        self.checks[turn] = False

    # SET <TUPLE>
    def getPieces(self, who):
        pces = set()
        for i in range(8):
            for j in range(8):
                if self.board[i][j].color == who:
                    pces.add(self.board[i][j])
        return pces

    # TUPLE
    def kingPos(self, who):
        for i in range(8):
            for j in range(8):
                pce = self.board[i][j]
                if pce.type == "king" and pce.color == who:
                    return pce.coord

    def __getitem__(self, idx):
        return self.board[idx]

    def __setitem__(self, idx, value):
        self.board[idx] = value

    def __repr__(self):
        return f"{self.__module__}{type(self).__name__} object at {hex(id(self))}"

    def __str__(self):
        return np.array2string(self.board)

