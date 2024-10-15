import keyboard
from chessbot.app import (
    analyze_image,
    get_best_move,
    take_screenshot,
    initialize_chessbot,
)
from chessbot.board_detector import BoardDetector
from chessbot.config import ChessBotConfig
from chessbot.mouse import Mouse


def main(config: ChessBotConfig):
    templates, board_state, stockfish = initialize_chessbot(config)
    previous_fen = None

    def process_move():
        """Function that handles screenshot, board detection, and move execution."""
        print("Processing move...")
        nonlocal previous_fen
        screenshot = take_screenshot(config.screenshot_region)
        board_boundary = BoardDetector.detect_boundary(screenshot)
        if board_boundary is None:
            print("Board not found. Try again.")
            return

        current_fen = analyze_image(screenshot, board_boundary, templates, board_state)

        # Check if the board is empty or there is an issue detecting the FEN
        if current_fen == "8/8/8/8/8/8/8/8 w - - 0 1" or current_fen is None:
            print("Board not detected properly, or it is not the player's turn.")
            return

        if current_fen == previous_fen:
            print("No change detected.")
            return

        if config.debug:
            board_state.display()
    
        previous_fen = current_fen
        try:
            best_move = get_best_move(stockfish, current_fen)
            if best_move:
                print(f"Moving piece: {best_move}")
                Mouse.move_piece(board_boundary, best_move[:2], best_move[2:4])
                print("Move executed.")
        except Exception as e:
            print(f"Error: {e}")
            return

    print("Press 'F9' to trigger the bot to make a move.")
    keyboard.add_hotkey("F9", process_move)

    keyboard.wait()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser("Chessbot")

    parser.add_argument("--template_dir", type=str, default="./templates/chess.com", help="Path to the template directory")
    parser.add_argument("--engine_path", type=str, default="./bin/stockfish", help="Path to the Stockfish engine")
    parser.add_argument("--region", type=int, nargs=4, default=[0, 0, 1920, 1080], help="Region of the screen to capture")
    parser.add_argument("--elo", type=int, default=700, help="Elo rating of the Stockfish engine")
    parser.add_argument("--side", type=str, required=True, choices=["w", "b"], help="Side to play as (w for white, b for black)")
    parser.add_argument("--depth", type=int, default=30, help="Depth of the Stockfish engine")
    parser.add_argument("--skill_level", type=int, default=20, help="Skill level of the Stockfish engine")

    args = parser.parse_args()

    config = ChessBotConfig(
        template_dir=args.template_dir,
        stockfish_executable_path=args.engine_path,
        screenshot_region=args.region,
        engine_elo=args.elo,
        is_white=args.side == "w",
        depth=args.depth,
        skill_level=args.skill_level,
    )

    main(config)
