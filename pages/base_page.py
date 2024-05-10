import math
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput


class Page:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def open_url(self, url):
        self.driver.get(url)

    def click(self, *locator):
        self.driver.find_element(*locator).click()

    def find_element(self, *locator):
        return self.driver.find_element(*locator)

    def find_elements(self, *locator):
        return self.driver.find_elements(*locator)

    def input(self, text, *locator):
        self.driver.find_element(*locator).send_keys(text)

    def save_screenshot(self, name):
        self.driver.save_screenshot(f'{name}.png')

    def wait_for_element_click(self, *locator):
        self.wait.until(
            EC.element_to_be_clickable(locator),
            message=f'Element by {locator} not clickable'
        ).click()

    def wait_for_element_appear(self, *locator):
        element = self.wait.until(
            EC.presence_of_element_located(locator),
            message=f'Element by {locator} not appear'
        )
        return element

    def wait_for_element_disappear(self, *locator):
        self.wait.until(
            EC.invisibility_of_element_located(locator),
            message=f'Element by {locator} is still visible'
        )

    def wait_for_element_visible(self, *locator):
        element = self.wait.until(
            EC.visibility_of_element_located(locator),
            message=f'Element by {locator} not visible'
        )
        return element

    def verify_partial_text(self, expected_text, *locator):
        actual_text = self.find_element(*locator).text
        assert expected_text in actual_text, \
            f"Expected text {expected_text} not in actual {actual_text}"

    def verify_text(self, expected_text, *locator):
        actual_text = self.find_element(*locator).text
        assert expected_text == actual_text, \
            f"Expected text {expected_text} did not match actual {actual_text}"

    def click_by_element_coordinates(self, x_percent, y_percent, *locator):
        """
        Taps by coordinates, coordinates calculated based on element size and location
        :param x_percent: x position (in percent) to tap
        :param y_percent: y position (in percent) to tap
        :param locator: locator of the element to find
        """
        e = self.driver.find_element(*locator)
        size = e.size
        location = e.location

        width, height = size['width'], size['height']
        location_x, location_y = location['x'], location['y']
        tap_x = math.floor(location_x + width * x_percent / 100)
        tap_y = math.floor(location_y + height * y_percent / 100)

        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(self.driver,
                                            mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(x=tap_x, y=tap_y)
        actions.w3c_actions.pointer_action.click()
        actions.w3c_actions.perform()
