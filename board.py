import numpy as np
from pieces import *


class Board:
    def __init__(self):
        self.board = np.empty((8, 8), dtype=np.object)
        self.turn = 1

        self.selected = None
        self.moved = False
        self.start = None
        self.end = None
        self.allowed = set()
        self.updates = {1: False, -1: False}
        self.captured = {1: [], -1: []}
        self.kpos = None

        self.checks = {1: 0, -1: 0}
        self.pins = set()
        self.blockslots = set()

    def setup(self) -> None:
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

    def update_went(self, player) -> None:
        self.updates[player] = True
        if self.updates[1] and self.updates[-1]:
            self.moved = False
            self.updates[-1] = False
            self.updates[1] = False
            self.selected = None

    def pending_update(self, player) -> bool:
        return not self.updates[player]

    def move(self, row, col) -> None:
        if (newPos := (row, col)) in self.allowed:
            oldPos = self.selected.coord
            if self.has_piece(row, col):
                self.captured[self.turn].append(self.board[newPos])
                self.board[newPos] = self.board[oldPos]
                self.board[oldPos] = Empty(0)
            else:
                self.board[newPos], self.board[oldPos] = self.board[oldPos], self.board[newPos]

            self.board[newPos].set_pos(newPos)

            if isinstance(self.board[newPos], King) or isinstance(self.board[newPos], Pawn):
                self.board[newPos].update_moved(True)

            self.moved = True
            self.end = newPos
            self.switch_turn()
            self.check_logic()

    def is_checked(self):
        return self.checks[self.turn] > 0

    def is_mine(self, row, col) -> bool:
        return self.board[row][col].color == self.turn

    def set_selected(self, piece: Piece) -> None:
        self.selected = piece
        self.start = piece.coord

    def store_allowed(self) -> None:
        self.allowed.clear()
        if self.selected.coord not in self.pins:
            if self.checks[self.turn] >= 2 and self.selected.type == "King":
                self.allowed = self.king_filter()
            elif self.checks[self.turn] == 1:
                if self.selected.type == "King":
                    self.allowed = self.king_filter()
                else:
                    self.allowed = self.selected.get_moves(self.board).intersection(self.blockslots)
            else:
                self.allowed = self.selected.get_moves(self.board)

    def king_filter(self) -> set:
        kingmoves = self.piece_at(*self.kpos).get_moves(self.board)
        oppomoves = set()
        for coord in Piece.allpos[-self.turn]:
            moves = self.piece_at(*coord).get_moves(self.board)
            oppomoves.update(moves)
        # RETURN WHAT KINGMOVES HAS THAT OPPOMOVES DOES NOT HAVE
        return kingmoves.difference(oppomoves)

    def check_logic(self) -> None:
        self.checks[self.turn] = 0
        self.pins.clear()
        self.blockslots.clear()
        self.kpos = Piece.kingpos[self.turn]
        krow, kcol = self.kpos
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
                            self.checks[self.turn] += 1

    def step_away(self, row, col, rmul, cmul) -> None:
        step = 0
        blockslot = set()
        check = False
        pinCount = 0
        pin = None
        while True:
            step += 1
            nrow = row + (step * rmul)
            ncol = col + (step * cmul)
            if 0 <= nrow <= 7 and 0 <= ncol <= 7:
                pce = self.piece_at(nrow, ncol)
                if pce.color == 0:
                    blockslot.add((nrow, ncol))
                elif pce.color == self.turn:
                    pinCount += 1
                    pin = (nrow, ncol)
                else:
                    if (
                        pce.type == "Queen"
                        or (pce.type == "Rook" and abs(rmul) != abs(cmul))
                        or (pce.type == "Bishop" and abs(rmul) == abs(cmul))
                        or (pce.type == "Pawn" and abs(cmul) == 1 and nrow == row + pce.color)
                    ):
                        self.checks[self.turn] += 1
                        check = True
                        break
            else:
                break
        if check:
            if pinCount == 0:
                self.blockslots.update(blockslot)
            else:
                self.checks[self.turn] -= 1
                if pinCount == 1:
                    self.pins.add(pin)

    def piece_at(self, row, col) -> Piece:
        return self.board[int(row)][int(col)]

    def switch_turn(self) -> None:
        self.turn *= -1

    def has_piece(self, row, col) -> bool:
        return isinstance(self.piece_at(row, col), Piece)

    def __str__(self) -> str:
        strboard = []
        for row in self.board:
            for piece in row:
                strboard.append(f" {str(piece)[:3]} ")
            strboard.append("\n")
        return "".join(strboard)
