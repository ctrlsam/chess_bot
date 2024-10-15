import cv2
import numpy as np
from chessbot.board_state import BoardState


class PieceDetector:

    @staticmethod
    def update_board(
        board_image: np.ndarray, templates: dict, board_state: BoardState
    ) -> None:
        squares = PieceDetector.extract_squares(board_image)

        board_state.board.clear()

        for i, row in enumerate(squares):
            for j, square in enumerate(row):
                match = PieceDetector.match_template(square, templates)
                if match:
                    board_state.set_piece(i, j, match)

    @staticmethod
    def extract_squares(board_image: np.ndarray) -> list[list[np.ndarray]]:
        squares = []
        square_size = board_image.shape[0] // 8

        for row in range(8):
            row_squares = []
            for col in range(8):
                square = board_image[
                    row * square_size : (row + 1) * square_size,
                    col * square_size : (col + 1) * square_size,
                ]
                row_squares.append(square)
            squares.append(row_squares)

        return squares

    @staticmethod
    def preprocess_image(image: np.ndarray) -> np.ndarray:
        image = cv2.resize(image, (64, 64))
        if len(image.shape) == 3 and image.shape[2] == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        elif len(image.shape) == 2:
            gray = image
        else:
            raise ValueError(f"Unexpected image shape: {image.shape}")

        blurred = cv2.GaussianBlur(gray, (5, 5), 0)  # Apply Gaussian Blur
        edges = cv2.Canny(blurred, 50, 150)  # Apply Canny Edge Detection
        return edges

    @staticmethod
    def get_color_mask(image: np.ndarray, color: str) -> np.ndarray:
        # Convert to HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        if color == "w":
            # Define range for white color in HSV
            lower = np.array([0, 0, 200])
            upper = np.array([180, 25, 255])
        else:
            # Adjusted range for black color
            lower = np.array([0, 0, 0])
            upper = np.array([180, 255, 240])
        mask = cv2.inRange(hsv, lower, upper)

        return mask

    @staticmethod
    def match_template(square: np.ndarray, templates: dict) -> tuple[str, str] | None:
        best_match = None
        best_score = 0

        for color in ["b", "w"]:
            color_mask = PieceDetector.get_color_mask(square, color)
            masked_square = cv2.bitwise_and(square, square, mask=color_mask)
            preprocessed_masked_square = PieceDetector.preprocess_image(masked_square)

            for piece, template in templates[color].items():
                # Preprocess the template
                preprocessed_template = PieceDetector.preprocess_image(template)
                # Perform template matching
                res = cv2.matchTemplate(
                    preprocessed_masked_square,
                    preprocessed_template,
                    cv2.TM_CCOEFF_NORMED,
                )
                _, max_val, _, _ = cv2.minMaxLoc(res)

                if max_val > best_score:
                    best_score = max_val
                    best_match = (color, piece)

        if best_score > 0.1:
            return best_match
        return None
