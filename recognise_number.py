import cv2
import os
import numpy as np
from score import score_region


def compare_digits(filename):
    # Load digit database
    digit_database = {}
    for i in range(10):
        digit_path = os.path.join("database/digits", f"{i}.png")
        digit_image = cv2.imread(digit_path, cv2.IMREAD_GRAYSCALE)
        digit_image_resized = cv2.resize(digit_image, (12, 25))
        digit_image_resized = digit_image_resized / 255.0  # Normalize the digit image
        digit_database[i] = digit_image_resized

    # Preprocess the input image
    image_path = score_region(filename)
    image = cv2.imread(image_path)  # Load the image
    image_array = np.array(image)  # Convert image to numpy array
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, image_thresh = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY_INV)

    # Recognize individual digits
    digits = []
    contours, _ = cv2.findContours(
        image_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        print(x, y, w, h)
        digit_roi = image_thresh[y : y + h, x : x + w]
        digit_roi_resized = cv2.resize(digit_roi, (12, 25))
        digit_roi_resized = digit_roi_resized / 255.0  # Normalize the digit image
        digit_roi_resized = digit_roi_resized.reshape(1, 25, 12, 1)

        # Compare the digit with the digit database
        max_similarity = float("inf")
        recognized_digit = None
        for digit, digit_image in digit_database.items():
            similarity = cv2.matchShapes(
                digit_image, digit_roi_resized, cv2.CONTOURS_MATCH_I3, 0
            )
            if similarity < max_similarity:
                max_similarity = similarity
                recognized_digit = digit

        digits.append(recognized_digit)

    # Convert the recognized digits to an integer number
    number = int("".join(map(str, digits)))

    return number


if __name__ == "__main__":
    image_path = "./database/screenshots/ss0.png"

    number = compare_digits(image_path)
    print(number)
