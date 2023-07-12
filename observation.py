import cv2
import numpy as np
import time


def score_region(filename):
    # Load screenshot image
    screenshot = cv2.imread(filename)

    NUM_OF_COL = 10
    NUM_OF_ROW = 20
    box_height, box_width = 26, 26

    # Region of interest
    x = 830  # Top-left x-coordinate of the ROI
    y = 475  # Top-left y-coordinate of the ROI
    width = 260  # Width of the ROI
    height = 520  # Height of the ROI

    # Extract the score region from the screenshot
    score_region = screenshot[y : y + height, x : x + width]
    gray_image = cv2.cvtColor(score_region, cv2.COLOR_BGR2GRAY)

    # Create a 2D NumPy array to represent the gameboard
    gameboard = np.zeros((NUM_OF_ROW, NUM_OF_COL), dtype=np.uint8)

    # Iterate over the gameboard boxes and read one pixel from each box
    for i in range(NUM_OF_ROW):
        for j in range(NUM_OF_COL):
            x = j * box_width + box_width // 2
            y = i * box_height + box_height // 2
            pixel_value = gray_image[
                y, x
            ]  # Read the pixel value at the center of the box
            if pixel_value == 0:  # Assuming 0 represents an empty box
                gameboard[i, j] = 0
            else:
                gameboard[i, j] = 1

    return gameboard


if __name__ == "__main__":
    start_time = time.time()
    print(score_region("screenshot/sample/380.png"))
    end_time = time.time()
    print(end_time - start_time)
