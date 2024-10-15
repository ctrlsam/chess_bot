from dataclasses import dataclass


@dataclass
class ChessBotConfig:
    template_dir: str
    stockfish_executable_path: str
    screenshot_region: tuple[int, int, int, int] | None = None
    engine_elo: int = 700
    is_white: bool = True
    depth: int = 2
    skill_level: int = 20
    debug: bool = False
 