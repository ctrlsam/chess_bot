import cv2


class PieceTemplate:
    def __init__(self, template_dir="templates/chess.com"):
        self.templates = {"b": {}, "w": {}}
        self.load_templates(template_dir)

    def load_templates(self, template_dir):
        piece_types = ["b", "k", "n", "p", "q", "r"]
        for color in ["b", "w"]:
            for piece in piece_types:
                path = f"{template_dir}/{color}{piece}.png"
                self.templates[color][piece] = cv2.imread(path)

    def get_templates(self):
        return self.templates
