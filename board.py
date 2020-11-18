import numpy as np
from pieces import *

fprint = lambda x: print(x, flush=True)


class Board:
    def __init__(self):
        self.board = np.empty((8, 8), dtype=np.object)
        self.turn = 1

        self.selected = None
        self.moved = False
        self.start = None
        self.dest = None
        self.updates = [None, False, False]
        self.allowed = set()
        self.captured = {1: [], -1: []}

        self.checks = 0
        self.pins = set()
        self.blockslots = set()

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

    def update_went(self, player):
        self.updates[player] = True
        if self.updates[1] and self.updates[-1]:
            self.moved = False
            self.updates[-1] = False
            self.updates[1] = False
            self.selected = None

    def pending_update(self, player):
        return not self.updates[player]

    def move(self, row, col):
        if (pos := (row, col)) in self.allowed:
            oldPos = self.selected.coord
            if self.has_piece(row, col):
                self.captured[self.turn].append(self.board[pos])
            self.board[pos] = self.board[oldPos]
            self.board[oldPos] = Empty(0)
            self.board[pos].set_pos(pos)

            if isinstance(self.board[pos], King) or isinstance(self.board[pos], Pawn):
                self.board[pos].update_moved(True)

            self.moved = True
            self.dest = pos
            self.switch_turn()

    def is_mine(self, row, col):
        return self.board[row][col].color == self.turn

    def set_selected(self, piece: Piece):
        self.selected = piece
        self.start = self.selected.coord

    def store_allowed(self):
        self.check_logic()
        if self.checks >= 2 and self.selected.type == "King":
            self.allowed = self.king_filter()
        elif self.checks == 1:
            if self.selected.type == "King":
                self.allowed = self.king_filter()
            else:
                self.allowed = self.selected.get_moves(self.board).intersection(self.blockslots)
        else:
            self.allowed = self.selected.get_moves(self.board)

    def king_filter(self):
        kpos = Piece.kingpos[self.turn]
        kingmoves = self.piece_at(*kpos).get_moves(self.board)
        oppomoves = set()
        for coord in Piece.allpos[self.turn * -1]:
            moves = self.piece_at(*coord).get_moves(self.board)
            oppomoves.update(moves)
        # RETURN WHAT KINGMOVES HAS THAT OPPOMOVES DOES NOT HAVE
        return kingmoves.difference(oppomoves)

    def check_logic(self):
        self.checks = 0
        self.blockslots.clear()
        krow, kcol = Piece.kingpos[self.turn]
        for rmul in range(-1, 2):
            for cmul in range(-1, 2):
                if rmul == 0 and cmul == 0:
                    continue
                self.step_away(krow, kcol, rmul, cmul)
        # KNIGHT CHECK
        tup = (2, 1)
        for i in range(2):
            for r in (krow + tup[i], krow - tup[i]):
                for c in (kcol + tup[i ^ 1], kcol - tup[i ^ 1]):
                    if 0 <= r <= 7 and 0 <= c <= 7:
                        pce = self.piece_at(r, c)
                        if pce.color == self.turn * -1 and pce.type == "Knight":
                            self.checks += 1

    def step_away(self, row, col, rmul, cmul):
        step = 0
        while True:
            step += 1
            nrow = row + (step * rmul)
            ncol = col + (step * cmul)
            if 0 <= nrow <= 7 and 0 <= ncol <= 7:
                pce = self.piece_at(nrow, ncol)
                if pce.color == 0:
                    self.blockslots.add((nrow, ncol))
                elif pce.color == self.turn:
                    # FIX PIN
                    return
                else:
                    if (
                        pce.type == "Queen"
                        or (pce.type == "Rook" and abs(rmul) != abs(cmul))
                        or (pce.type == "Bishop" and abs(rmul) == abs(cmul))
                        or (pce.type == "Pawn" and abs(cmul) == 1 and nrow == row + pce.color)
                    ):
                        self.checks += 1
                        return
            else:
                return

    def piece_at(self, row, col) -> Piece:
        return self.board[row][col]

    def switch_turn(self):
        self.turn *= -1

    def has_piece(self, row, col):
        return isinstance(self.board[int(row)][int(col)], Piece)

    def __str__(self):
        strboard = []
        for row in self.board:
            for piece in row:
                strboard.append(f" {str(piece)[:3]} ")
            strboard.append("\n")
        return "".join(strboard)


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
