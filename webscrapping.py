from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # Keypresses
import pyautogui  # Mouse clicks

import time
import subprocess


class Tetris:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.set_window_size(1920, 1080)
        self.driver.get("https://tetris.com/play-tetris")
        self.driver.implicitly_wait(10)  # Wait up to 10s for page to load

        iframe = self.driver.find_element(By.ID, "gameIFrame")
        self.driver.switch_to.frame(iframe)
        self.canvas = self.driver.find_element(By.ID, "GameCanvas")

        # New
        window_handle = self.driver.current_window_handle
        # window_id = int(window_handle)
        print(type(window_handle), window_handle)

    def start(self):
        # Close ads
        pyautogui.moveTo(30, 940)
        pyautogui.click()
        pyautogui.moveTo(850, 900)
        pyautogui.click()

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
        output_file = "browser_screenshot.png"
        command = f"import -window {window_id} {output_file}"
        subprocess.run(command, shell=True)

    def reset(self):
        pass

    def reward(self):
        # Returns the current score
        pass

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

# while True:
#     time.sleep(1)
#     tetris.perform_action(0)
