import cv2
import os
import numpy as np
from score import score_region


def get_score(filename):
    digit_database = {}
    for i in range(10):
        digit_path = os.path.join("database/digits", f"{i}.png")
        digit_image = cv2.imread(digit_path, cv2.IMREAD_GRAYSCALE)
        digit_image_resized = cv2.resize(digit_image, (12, 25))
        digit_image_resized = digit_image_resized / 255.0  # Normalize the digit image
        digit_database[i] = digit_image_resized

    image_path = score_region(filename)
    image = cv2.imread(image_path)
    print(image)


if __name__ == "__main__":
    get_score("./database/screenshots/ss0.png")
