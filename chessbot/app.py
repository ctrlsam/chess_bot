import cv2
import numpy as np
import pyautogui
from stockfish import Stockfish

from chessbot.board_detector import BoardDetector
from chessbot.config import ChessBotConfig
from chessbot.piece_template import PieceTemplate
from chessbot.piece_detector import PieceDetector
from chessbot.board_state import BoardState


def initialize_chessbot(config: ChessBotConfig):
    templates = PieceTemplate(template_dir=config.template_dir).get_templates()
    board_state = BoardState(side=config.is_white)
    stockfish = Stockfish(
        config.stockfish_executable_path,
        parameters={
            "Threads": 8,
            "Ponder": "true",
            "Minimum Thinking Time": 20000,
        },
    )
    stockfish.set_elo_rating(config.engine_elo)
    stockfish.set_skill_level(config.skill_level)
    stockfish.set_depth(config.depth)

    return templates, board_state, stockfish


def analyze_image(image: np.ndarray, boundary: np.ndarray, templates, board_state):
    board_image = BoardDetector.crop_to_boundary(image, boundary)
    return process_board_image(board_image, templates, board_state)


def get_best_move(stockfish: Stockfish, fen: str) -> str | None:
    stockfish.set_fen_position(fen)
    return stockfish.get_best_move()


def process_board_image(board_image, templates, board_state: BoardState):
    PieceDetector.update_board(board_image, templates, board_state)
    return board_state.get_board().fen()


def take_screenshot(region: tuple[int, int, int, int] | None) -> np.ndarray:
    screenshot = pyautogui.screenshot(region=region)
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
