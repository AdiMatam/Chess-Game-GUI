import numpy as np
from chsPieces import *


class Board:
    def __init__(self):
        self.board = np.empty((8, 8), dtype=np.object)

    def __getitem__(self, idx):
        return self.board[idx]

    def __setitem__(self, idx, value):
        self.board[idx] = value

    def __str__(self):
        print(*self.board, sep="\n", end="\n\n")
