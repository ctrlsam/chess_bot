import cv2
import numpy as np


class BoardDetector:
    @staticmethod
    def detect_boundary(image: np.ndarray) -> np.ndarray | None:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray_image, 50, 150)

        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        chessboard_contour = None
        max_area = 0
        for contour in contours:
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            if len(approx) == 4:
                area = cv2.contourArea(contour)
                if area > max_area:
                    max_area = area
                    chessboard_contour = approx

        return chessboard_contour

    @staticmethod
    def crop_to_boundary(image: np.ndarray, chessboard_contour: np.ndarray):
        # Get the bounding box of the chessboard
        pts = chessboard_contour.reshape(4, 2)

        # Determine the top-left, top-right, bottom-left, bottom-right corners
        rect = np.zeros((4, 2), dtype="float32")

        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]  # top-left
        rect[2] = pts[np.argmax(s)]  # bottom-right

        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]  # top-right
        rect[3] = pts[np.argmax(diff)]  # bottom-left

        # Get width and height of the chessboard
        width = height = 800

        dst = np.array(
            [[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]],
            dtype="float32",
        )

        # Apply perspective transformation
        matrix = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, matrix, (width, height))

        return warped

    @staticmethod
    def get_chessboard_rect(chessboard_contour: np.ndarray) -> cv2.typing.Rect:
        pts = chessboard_contour.reshape(4, 2)
        return cv2.boundingRect(pts)
