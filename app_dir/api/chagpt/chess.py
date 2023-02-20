class ChessPiece:
    def __init__(self, name, position):
        self.name = name
        self.position = position

    def move(self, new_position):
        self.position = new_position

class ChessBoard:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.setup_board()

    def setup_board(self):
        self.board[0][0] = ChessPiece("rook", (0, 0))
        self.board[0][1] = ChessPiece("knight", (0, 1))
        self.board[0][2] = ChessPiece("bishop", (0, 2))
        self.board[0][3] = ChessPiece("queen", (0, 3))
        self.board[0][4] = ChessPiece("king", (0, 4))
        self.board[0][5] = ChessPiece("bishop", (0, 5))
        self.board[0][6] = ChessPiece("knight", (0, 6))
        self.board[0][7] = ChessPiece("rook", (0, 7))
        self.board[1] = [ChessPiece("pawn", (1, i)) for i in range(8)]
        self.board[6] = [ChessPiece("pawn", (6, i)) for i in range(8)]
        self.board[7][0] = ChessPiece("rook", (7, 0))
        self.board[7][1] = ChessPiece("knight", (7, 1))
        self.board[7][2] = ChessPiece("bishop", (7, 2))
        self.board[7][3] = ChessPiece("queen", (7, 3))
        self.board[7][4] = ChessPiece("king", (7, 4))
        self.board[7][5] = ChessPiece("bishop", (7, 5))
        self.board[7][6] = ChessPiece("knight", (7, 6))
        self.board[7][7] = ChessPiece("rook", (7, 7))

    def move_piece(self, current_pos, new_pos):
        piece = self.board[current_pos[0]][current_pos[1]]
        if piece:
            piece.move(new_pos)
            self.board[current_pos[0]][current_pos[1]] = None
            self.board[new_pos[0]][new_pos[1]] = piece
            return True
        return False

board = ChessBoard()
print(board.move_piece((0, 1), (2, 0)))
print(board.board)
