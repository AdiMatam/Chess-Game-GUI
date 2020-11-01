import numpy as np
from pieces import *


class Board:
    def __init__(self):
        self.board = np.empty((8, 8), dtype=np.object)
        self.turn = 1

        self.selected = None
        self.allowed = set()
        self.captured = {1: [], -1: []}

    def setup(self):
        for idx in range(8):
            self.board[1][idx] = Pawn(-1, (1, idx))
            self.board[6][idx] = Pawn(1, (6, idx))

        row = (Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook)

        for idx, Item in enumerate(row):
            self.board[0][idx] = Item(-1, (0, idx))
            self.board[7][idx] = Item(1, (7, idx))

        for i in range(2, 6):
            for j in range(8):
                self.board[i][j] = Empty(0)

    def move(self, row, col):
        if (pos := (row, col)) in self.allowed:
            oldPos = self.selected.coord
            self.board[pos] = self.board[oldPos]
            self.board[oldPos] = Empty(0)
            self.board[pos].set_pos(pos)
            self.selected = None

    def is_mine(self, row, col):
        return self.board[row][col].color == self.turn

    def set_selected(self, piece: Piece):
        self.selected = piece

    def store_allowed(self):
        self.allowed = self.selected.get_moves(self.board)

    def piece_at(self, row, col) -> Piece:
        return self.board[row][col]

    def switch_turn(self):
        self.turn *= -1

    def has_piece(self, row, col):
        return isinstance(self.board[int(row)][int(col)], Piece)

    def __str__(self):
        return np.array2string(self.board)

    # def update_positions(self):
    #     self.allpos = Piece.allpos

    # def get_checked(self):
    #     self.update_positions()
    #     myposes = self.allpos.get(self.turn)
    #     oking = self.get_king(self.turn * -1)
    #     legals = set()
    #     for pos in myposes:
    #         legals.update(self.piece_at(*pos).get_moves(self.board))

    #     if oking.coord in legals:
    #         return oking

    # def get_king(self, turn=None) -> Piece:
    #     if not turn:
    #         turn = self.turn
    #     for pos in self.allpos.get(turn):
    #         if isinstance(self.board[pos], King) and self.board[pos].color == turn:
    #             return self.board[pos]
