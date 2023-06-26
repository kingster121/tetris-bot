from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # Detect keypresses

driver = webdriver.Firefox()
driver.get("https://tetris.com/play-tetris")
driver.implicitly_wait(10)  # Wait 10s for page to load


class Browser:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.get("https://tetris.com/play-tetris")

    def action_to_keys(i: int):
        actions_dict = {
            0: Keys.ARROW_UP,
            1: Keys.ARROW_DOWN,
            2: Keys.ARROW_LEFT,
            3: Keys.ARROW_RIGHT,
        }
        return actions_dict[i]


# action_to_keys(0)
