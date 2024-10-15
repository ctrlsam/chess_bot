import chess


class BoardState:
    def __init__(self, side: chess.Color = chess.WHITE):
        self.board = chess.Board()
        self.board.clear()
        self.side = side

    def set_piece(self, row: int, col: int, piece: tuple[str, str]):
        """
        Set a piece on the board.

        Parameters:
        - row: Row index (0 at the top to 7 at the bottom)
        - col: Column index (0 at the left to 7 at the right)
        - piece: Tuple (color, piece_type), e.g., ('w', 'k') for white king
        """
        # Map (row, col) to chess square
        square = chess.square(col, 7 - row)

        # Map piece type to chess.PieceType
        piece_type_map = {
            "k": chess.KING,
            "q": chess.QUEEN,
            "r": chess.ROOK,
            "b": chess.BISHOP,
            "n": chess.KNIGHT,
            "p": chess.PAWN,
        }
        piece_type = piece_type_map.get(piece[1].lower())

        self.board.turn = self.side

        if piece_type is not None:
            chess_piece = chess.Piece(piece_type, piece[0] == "w")
            self.board.set_piece_at(square, chess_piece)

        else:
            pass  # Invalid piece type

    def get_board(self):
        return self.board

    def display(self):
        print(self.board)
