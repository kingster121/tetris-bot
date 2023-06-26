from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # Keypresses

import time
import pyautogui  # Mouse clicks


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
        # Close ad
        pyautogui.moveTo(30, 940)
        pyautogui.click()

        # Start game
        pyautogui.moveTo(900, 680)
        pyautogui.click()

    def reset(self):
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

while True:
    time.sleep(1)
    tetris.perform_action(0)
