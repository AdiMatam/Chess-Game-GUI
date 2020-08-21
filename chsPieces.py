class Piece:
    def __init__(self, color: int, coord: tuple):
        self.color = color
        self.coord = coord
        self.type = type(self).__name__

        self.colorDict = {1: "w", -1: "b"}
        self.image = f"images\{self.colorDict[color]}{self.type}.png".lower()

    # VOID
    def updatePos(self, newCoord: tuple):
        self.coord = newCoord

    # BOOLEAN
    def checkBound(self, x, y):
        if 0 <= x < 8 and 0 <= y < 8:
            return True
        return False

    # SET <TUPLE>
    def applyMuls(self, board, rowMul, colMul):
        currentMoves = set()
        step = 0
        row, col = self.coord
        while True:
            step += 1
            newRow = row + (rowMul * step)
            newCol = col + (colMul * step)

            if self.checkBound(newRow, newCol):
                if (color := board[newRow][newCol].color) != self.color:
                    currentMoves.add((newRow, newCol))
                    if color == self.color * -1:
                        break
                else:
                    break
            else:
                break

        return currentMoves

    # STR
    def __str__(self):
        return f"{self.color} {self.type} at {self.coord}"


class Pawn(Piece):
    def __init__(self, color, coord: tuple):
        super().__init__(color, coord)
        self.moved = False

    def getMoves(self, board):
        allowed = set()
        row, col = self.coord

        nextRow = row + (self.color * -1)  # subtracts for "wht", adds for "blk"

        # iter thru diag-left, straight-ahead, diag-right
        for offset in range(-1, 2, 1):
            if col + offset < 0 or col + offset > 7:
                continue
            loc = (nextRow, col + offset)
            if offset == 0:  # straight-ahead
                if board[loc].color == 0:
                    allowed.add((loc))
            else:
                if board[loc].color == self.color * -1:
                    allowed.add((loc))

        double = (row + (self.color * -2), col)  # coordinates for pawn-double-step

        if board[double].color == 0 and not self.moved:
            allowed.add(double)

        return allowed

    def updateMoved(self, moved):
        self.moved = moved


class Bishop(Piece):
    def __init__(self, color, coord: tuple):
        super().__init__(color, coord)

    def getMoves(self, board):
        allowed = set()

        for rowMul in (-1, 1):
            for colMul in (-1, 1):
                moveSet = self.applyMuls(board, rowMul, colMul)
                allowed.update(moveSet)

        return allowed


class Knight(Piece):
    def __init__(self, color, coord: tuple):
        super().__init__(color, coord)

    def getMoves(self, board):
        allowed = set()
        row, col = self.coord

        add = [2, 1]

        for i in range(2):
            for r in (row + add[i], row - add[i]):
                for c in (col + add[i ^ 1], col - add[i ^ 1]):
                    if self.checkBound(r, c):
                        if board[r][c].color != self.color:
                            allowed.add((r, c))

        return allowed


class Rook(Piece):
    def __init__(self, color, coord: tuple):
        super().__init__(color, coord)

    def getMoves(self, board):
        allowed = set()

        for rowMul in range(-1, 2):
            for colMul in range(-1, 2):
                if abs(rowMul) == abs(colMul):
                    continue
                moveSet = self.applyMuls(board, rowMul, colMul)
                allowed.update(moveSet)

        return allowed


class Queen(Piece):
    def __init__(self, color, coord: tuple):
        super().__init__(color, coord)

    def getMoves(self, board):
        allowed = set()

        for rowMul in range(-1, 2):
            for colMul in range(-1, 2):
                moveSet = self.applyMuls(board, rowMul, colMul)
                allowed.update(moveSet)

        return allowed


class King(Piece):
    def __init__(self, color, coord: tuple):
        super().__init__(color, coord)
        self.castle = False
        self.moved = False
        self.checked = False

    def getMoves(self, board):
        allowed = set()
        row, col = self.coord

        for r in range(-1, 2):
            for c in range(-1, 2):
                rIdx = row + r
                cIdx = col + c
                if self.checkBound(rIdx, cIdx):
                    if board[rIdx][cIdx].color != self.color:
                        allowed.add((rIdx, cIdx))

        # CASTLE

    def updateMoved(self, moved):
        self.moved = moved


class Empty:
    def __init__(self, color: int):
        self.color = color
