import cv2


def score_region(filename):
    # Load screenshot image
    print(filename)
    screenshot = cv2.imread(filename)

    # Define the region of interest (ROI) coordinates containing the score
    x = 650  # Top-left x-coordinate of the ROI
    y = 815  # Top-left y-coordinate of the ROI
    width = 110  # Width of the ROI
    height = 25  # Height of the ROI

    # Extract the score region from the screenshot
    score_region = screenshot[y : y + height, x : x + width]

    output_file = "./score_region.png"
    cv2.imwrite(output_file, score_region)

    return output_file


if __name__ == "__main__":
    score_region("./database/screenshots/ss0.png")
