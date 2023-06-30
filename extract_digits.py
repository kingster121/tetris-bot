import cv2

for i in range(10):
    # Load the screenshot image
    screenshot = cv2.imread(f"./numbers/score_regions/{i}.png")

    # Define the region of interest (ROI) coordinates containing the score
    x = 50  # Top-left x-coordinate of the ROI
    y = 0  # Top-left y-coordinate of the ROI
    width = 12  # Width of the ROI
    height = 25  # Height of the ROI

    # Extract the score region from the screenshot
    score_region = screenshot[y : y + height, x : x + width]

    cv2.imwrite(f"./numbers/digits/{i}.png", score_region)
