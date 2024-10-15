import unittest
import cv2
from chessbot.app import initialize_chessbot, analyze_image
from chessbot.board_detector import BoardDetector
from chessbot.config import ChessBotConfig


class TestChessBot(unittest.TestCase):

    def setUp(self):
        """Set up necessary components for testing."""
        self.template_dir = "./templates/chess.com"
        self.engine_path = "./bin/stockfish"
        self.templates, self.board_state, self.stockfish = (
            initialize_chessbot(ChessBotConfig(self.template_dir, self.engine_path))
        )

    def test_board_state_from_image(self):
        """Test that the board state is correctly detected from an image."""
        expected_fen = "rnbqkb1r/5p1p/p6n/2ppp1N1/2p2PP1/4P3/PPQPB1P1/RNB1K2R w - - 0 1"

        # Analyze the test image
        image = cv2.imread("./tests/assets/chess.com_1.png")
        board_boundary = BoardDetector.detect_boundary(image)
        assert board_boundary is not None, "Board boundary not found"
        actual_fen = analyze_image(
            image, board_boundary, self.templates, self.board_state
        )

        # Assert that the board state (FEN) is as expected
        self.assertEqual(actual_fen, expected_fen)

    def test_board_state_from_image_2(self):
        """Test that the board state is correctly detected from an image."""
        expected_fen = (
            "r1bqkbnr/1p3ppp/2n1p3/pBpp4/5P2/2N1PN2/PPPP2PP/R1BQK2R w - - 0 1"
        )

        # Analyze the test image
        image = cv2.imread("./tests/assets/chess.com_2.png")
        board_boundary = BoardDetector.detect_boundary(image)
        assert board_boundary is not None, "Board boundary not found"
        actual_fen = analyze_image(
            image, board_boundary, self.templates, self.board_state
        )

        # Assert that the board state (FEN) is as expected
        self.assertEqual(actual_fen, expected_fen)

    def test_board_state_from_image_3(self):
        """Test that the board state is correctly detected from an image."""
        expected_fen = "6nr/3N1k1p/2Q2P2/p7/6p1/1P2P1P1/P1PP3P/R3KR2 w - - 0 1"

        # Analyze the test image
        image = cv2.imread("./tests/assets/chess.com_3.png")
        board_boundary = BoardDetector.detect_boundary(image)
        assert board_boundary is not None, "Board boundary not found"
        actual_fen = analyze_image(
            image, board_boundary, self.templates, self.board_state
        )

        # Assert that the board state (FEN) is as expected
        self.assertEqual(actual_fen, expected_fen)

    def test_board_state_from_image_4(self):
        """Test that the board state is correctly detected from an image."""
        expected_fen = "3k1b2/1Q2ppr1/p3p3/p3P1P1/3P3p/4B3/PP4PP/4KR2 w - - 0 1"

        # Analyze the test image
        image = cv2.imread("./tests/assets/chess.com_4.png")
        board_boundary = BoardDetector.detect_boundary(image)
        assert board_boundary is not None, "Board boundary not found"
        actual_fen = analyze_image(
            image, board_boundary, self.templates, self.board_state
        )

        # Assert that the board state (FEN) is as expected
        self.assertEqual(actual_fen, expected_fen)


if __name__ == "__main__":
    unittest.main()
