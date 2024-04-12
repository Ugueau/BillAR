import cv2
import numpy as np
from Model.Queue import ImageCorner

STRAIGHTNESS_THRESHOLD = 60

# Return the side where there is the bluest pixel (end of the cue stick)
def find_end_of_cue_stick(image):
    # Convert the image to HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds of the blue color in HSV
    lower_blue = np.array([95, 50, 50])
    upper_blue = np.array([100, 255, 255])

    # Create a mask
    mask = cv2.inRange(hsv_image, lower_blue, upper_blue)

    # Calculate the sum of blue pixels in each corner
    sums = [
        np.sum(mask[:image.shape[0] // 2, :image.shape[1] // 2]),
        np.sum(mask[:image.shape[0] // 2, image.shape[1] // 2:]),
        np.sum(mask[image.shape[0] // 2:, :image.shape[1] // 2]),
        np.sum(mask[image.shape[0] // 2:, image.shape[1] // 2:])
    ]

    # Find the corner with the maximum sum
    max_corner = np.argmax(sums)
    # Highlight the side with the most blue
    if max_corner == 0:
        cv2.rectangle(image, (0, 0), (image.shape[1] // 2, image.shape[0] // 2), (130, 255, 255), 2)
        if abs(sums[0] - sums[1]) * 100 / sums[0] < STRAIGHTNESS_THRESHOLD:
            return ImageCorner.TOP
        elif abs(sums[0] - sums[2]) * 100 / sums[0] < STRAIGHTNESS_THRESHOLD:
            return ImageCorner.LEFT
        return ImageCorner.TOP_LEFT

    elif max_corner == 1:
        cv2.rectangle(image, (image.shape[1] // 2, 0), (image.shape[1], image.shape[0] // 2), (130, 255, 255), 2)
        if abs(sums[1] - sums[0]) * 100 / sums[1] < STRAIGHTNESS_THRESHOLD:
            return ImageCorner.TOP
        elif abs(sums[1] - sums[3]) * 100 / sums[1] < STRAIGHTNESS_THRESHOLD:
            return ImageCorner.RIGHT
        return ImageCorner.TOP_RIGHT

    elif max_corner == 2:
        if abs(sums[2] - sums[3]) * 100 / sums[2] < STRAIGHTNESS_THRESHOLD:
            return ImageCorner.BOTTOM
        elif abs(sums[2] - sums[0]) * 100 / sums[2] < STRAIGHTNESS_THRESHOLD:
            return ImageCorner.LEFT
        cv2.rectangle(image, (0, image.shape[0] // 2), (image.shape[1] // 2, image.shape[0]), (130, 255, 255), 2)
        return ImageCorner.BOTTOM_LEFT

    elif max_corner == 3:
        if abs(sums[3] - sums[1]) * 100 / sums[3] < STRAIGHTNESS_THRESHOLD:
            return ImageCorner.RIGHT
        elif abs(sums[3] - sums[2]) * 100 / sums[3] < STRAIGHTNESS_THRESHOLD:
            return ImageCorner.BOTTOM
        cv2.rectangle(image, (image.shape[1] // 2, image.shape[0] // 2), (image.shape[1], image.shape[0]),
                      (130, 255, 255),
                      2)
        return ImageCorner.BOTTOM_RIGHT


def get_side_coordinate(side, x1, y1, x2, y2):
    if side == ImageCorner.TOP_LEFT:
        return x1, y1
    elif side == ImageCorner.TOP:
        return (x1 + x2) / 2, y1
    elif side == ImageCorner.TOP_RIGHT:
        return x2, y1
    elif side == ImageCorner.RIGHT:
        return x2, (y1 + y2) / 2
    elif side == ImageCorner.BOTTOM_RIGHT:
        return x2, y2
    elif side == ImageCorner.BOTTOM:
        return (x1 + x2) / 2, y2
    elif side == ImageCorner.BOTTOM_LEFT:
        return x1, y2
    elif side == ImageCorner.LEFT:
        return x1, (y1 + y2) / 2


def get_opposite_side_coordinate(side, x1, y1, x2, y2):
    if side == ImageCorner.TOP_LEFT:
        return x2, y2
    elif side == ImageCorner.TOP:
        return (x1 + x2) / 2, y2
    elif side == ImageCorner.TOP_RIGHT:
        return x1, y2
    elif side == ImageCorner.RIGHT:
        return x1, (y1 + y2) / 2
    elif side == ImageCorner.BOTTOM_RIGHT:
        return x1, y1
    elif side == ImageCorner.BOTTOM:
        return (x1 + x2) / 2, y1
    elif side == ImageCorner.BOTTOM_LEFT:
        return x2, y1
    elif side == ImageCorner.LEFT:
        return x2, (y1 + y2) / 2