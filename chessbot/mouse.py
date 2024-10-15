import random
import time
import cv2
import numpy as np
import pyautogui

from chessbot.board_detector import BoardDetector


class Mouse:
    @staticmethod
    def move_piece(board_boundary: np.ndarray, from_square: str, to_square: str):
        board_rect = BoardDetector.get_chessboard_rect(board_boundary)

        # Click and drag to move the piece to destination
        from_rect = Mouse._get_rect_from_coord(board_rect, from_square)
        to_rect = Mouse._get_rect_from_coord(board_rect, to_square)
        from_center = Mouse._get_center_of_rect(from_rect)
        to_center = Mouse._get_center_of_rect(to_rect)

        # Move the mouse to the center of the 'from' square
        Mouse.human_like_move(from_center)
        pyautogui.mouseDown()
        time.sleep(random.uniform(0.1, 0.3))  # Randomize click hold time

        # Move the mouse to the center of the 'to' square
        Mouse.human_like_move(to_center)
        pyautogui.mouseUp()
        time.sleep(random.uniform(0.1, 0.3))  # Randomize release time

    @staticmethod
    def human_like_move(target_position: tuple[int, int], duration_base=0.25):
        current_position = pyautogui.position()

        # Adding small random deviations to simulate human movement
        deviation_factor = 10  # Max deviation in pixels
        intermediate_position = (
            current_position[0] + random.uniform(-deviation_factor, deviation_factor),
            current_position[1] + random.uniform(-deviation_factor, deviation_factor),
        )

        # Randomize the time it takes to move to each point
        random_duration = duration_base + random.uniform(-0.1, 0.2)

        # Move to an intermediate position first (randomised)
        pyautogui.moveTo(
            intermediate_position[0], intermediate_position[1], duration=random_duration
        )

        # Move to the final target position (with another random time)
        final_duration = random_duration + random.uniform(0.05, 0.15)
        pyautogui.moveTo(
            target_position[0], target_position[1], duration=final_duration
        )

    @staticmethod
    def _get_rect_from_coord(
        board_screen_rect: cv2.typing.Rect, coord: str
    ) -> tuple[int, int, int, int]:
        assert len(coord) == 2, "Coordinate must be a 2-character string"

        col, row = coord
        col = ord(col) - ord("a")  # Convert 'a' to 0, 'b' to 1, etc.

        screen_top_left_x = board_screen_rect[0]
        screen_top_left_y = board_screen_rect[1]
        square_size = board_screen_rect[2] // 8

        return (
            screen_top_left_x + square_size * col,
            screen_top_left_y + square_size * (8 - int(row)),
            square_size,
            square_size,
        )

    @staticmethod
    def _get_center_of_rect(rect: tuple[int, int, int, int]) -> tuple[int, int]:
        return rect[0] + rect[2] // 2, rect[1] + rect[3] // 2
