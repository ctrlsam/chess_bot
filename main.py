import cv2
from cv2 import Mat
import numpy as np
from src.piece import Piece


def load_pieces(site: str, screenshot: Mat, is_black: bool):
    color = 'black' if is_black else 'white'
    path = f'assets/{site}/{color}/'

    pieces = {}
    pieces['pawns'] = get_pieces(path+'pawn_2.png', screenshot)

    return pieces

def group_locations(piece_locations, piece_width, piece_height):
    rectangles = []
    for (x, y) in piece_locations: # add twice to allow rect grouping
        rectangles.append([int(x), int(y), int(piece_width), int(piece_height)])
        rectangles.append([int(x), int(y), int(piece_width), int(piece_height)])

    rectangles, _ = cv2.groupRectangles(rectangles, 1, 0.2)
    return rectangles

def is_black(screenshot: Mat, rectangle):
    [x, y, w, h] = rectangle
    x_center = x+int(w/2)
    y_center = y+int(h/2)
    color = screenshot[y_center][x_center][0]
    return color < 200

def get_pieces(img_path: str, screenshot: Mat, threshold=0.96):
    piece_image = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    piece_height, piece_width = piece_image.shape[:2]

    piece = piece_image[:,:,0:3]
    alpha = piece_image[:,:,3]
    alpha = cv2.merge([alpha,alpha,alpha])

    result = cv2.matchTemplate(screenshot, piece, cv2.TM_CCORR_NORMED, mask=alpha)

    y_locations, x_locations = np.where(result >= threshold)
    rectangles = group_locations(
        zip(x_locations, y_locations), piece_width, piece_height)

    pieces = []
    for rectangle in rectangles:
        [x, y, w, h] = rectangle
        center_x = x+int(w/2)
        center_y = y+int(h/2)
        color = is_black(screenshot, rectangle)
        pieces.append(Piece(center_x, center_y, piece_width, piece_height, color))

    return pieces


if __name__ == '__main__':
    screenshot = cv2.imread('source_example.png')
    
    black_pieces = load_pieces('chess.com', screenshot, True)
    for piece in black_pieces['pawns']:
        piece.draw(screenshot)

    cv2.imshow('Board', screenshot)
    cv2.waitKey()
    cv2.destroyAllWindows()