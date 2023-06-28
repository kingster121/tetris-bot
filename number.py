import cv2

# Load the screenshot image
screenshot = cv2.imread("./images/score7.png")

# Define the region of interest (ROI) coordinates containing the score
x = 650  # Top-left x-coordinate of the ROI
y = 815  # Top-left y-coordinate of the ROI
width = 110  # Width of the ROI
height = 25  # Height of the ROI

# Extract the score region from the screenshot
score_region = screenshot[y : y + height, x : x + width]

cv2.imwrite("./images/score_region.png", score_region)
