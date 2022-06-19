import cv2
from cv2 import Mat

class Piece:
    def __init__(self, x: int, y: int, w: int, h: int, is_black: bool):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.is_black = is_black

    def draw(self, image: Mat):
        color = (255,0,0) if self.is_black else (0,255,0)
        top_left = (self.x - int(self.w/2), self.y - int(self.h/2))
        bottom_right = (self.x + int(self.w/2), self.y + int(self.h/2))
        cv2.rectangle(
            image, top_left, bottom_right, color, 2)