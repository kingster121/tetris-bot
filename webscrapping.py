from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # Keypresses
import pyautogui  # Mouse clicks

import time
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
        if result:
            number = int("".join(filter(str.isdigit, result)))
            return number
        else:
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
