from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # Keypresses
import pyautogui  # Mouse clicks

import time
import numpy as np
import subprocess
import cv2
import pytesseract

SCREENSHOT_PATH = "./screenshot/browser_screenshot.png"


class Tetris:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.set_window_size(1920, 1080)
        self.driver.get("https://tetris.com/play-tetris")
        self.driver.implicitly_wait(10)  # Wait up to 10s for page to load

        iframe = self.driver.find_element(By.ID, "gameIFrame")
        self.driver.switch_to.frame(iframe)
        self.canvas = self.driver.find_element(By.ID, "GameCanvas")

    def start(self):
        # Close ads
        pyautogui.moveTo(30, 940)
        pyautogui.click()
        pyautogui.moveTo(850, 900)
        pyautogui.click()
        time.sleep(2)

        # Start game
        pyautogui.moveTo(900, 680)
        pyautogui.click()

    def screenshot(self):
        # Finds the window ID
        window_name = "Play Tetris"
        command = f"xdotool search --name '{window_name}'"
        output = subprocess.check_output(command, shell=True).decode("utf-8").strip()
        window_id = int(output)

        # Screenshot the window
        output_file = SCREENSHOT_PATH
        command = f"import -window {window_id} {output_file}"
        subprocess.run(command, shell=True)

    def reset(self):
        pass

    def observation(self):
        screenshot = cv2.imread(SCREENSHOT_PATH)

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

    def reward(self):
        # Returns the current score
        screenshot = cv2.imread(SCREENSHOT_PATH)

        # Define the region of interest (ROI) coordinates containing the score
        x = 650  # Top-left x-coordinate of the ROI
        y = 815  # Top-left y-coordinate of the ROI
        width = 110  # Width of the ROI
        height = 25  # Height of the ROI

        # Extract the score region from the screenshot
        score_region = screenshot[y : y + height, x : x + width]

        # Convert the image to grayscale
        gray_image = cv2.cvtColor(score_region, cv2.COLOR_BGR2GRAY)

        # Use Tesseract OCR to extract text from the image
        result = pytesseract.image_to_string(gray_image, config="--psm 6")

        # Process the result to extract the number
        try:
            number = int("".join(filter(str.isdigit, result)))
            return number
        except:
            return 0

    def action_to_keys(self, i: int):
        actions_dict = {
            0: Keys.ARROW_UP,
            1: Keys.ARROW_DOWN,
            2: Keys.ARROW_LEFT,
            3: Keys.ARROW_RIGHT,
        }
        return actions_dict[i]

    def perform_action(self, i: int):
        key = self.action_to_keys(i)
        self.canvas.send_keys(key)


tetris = Tetris()
time.sleep(10)
tetris.start()

while True:
    time.sleep(1)
    tetris.screenshot()
    print(tetris.reward())
