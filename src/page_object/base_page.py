from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ex_cond


def get_locator_by_string(locator_with_type):
    exploided_locator = locator_with_type.split(':', 1)
    by_type = exploided_locator[0]
    locator = exploided_locator[1]

    if by_type == 'xpath':
        return (MobileBy.XPATH, locator)
    elif by_type == 'id':
        return (MobileBy.ID, locator)
    elif by_type == 'accessibility_id':
        return (MobileBy.ACCESSIBILITY_ID, locator)
    elif by_type == 'android_uiautomator':
        return (MobileBy.ANDROID_UIAUTOMATOR, locator)
    else:
        raise Exception(f'Cannot get type of locator. Locator {locator_with_type}')


class BasePage:

    def __init__(self, driver: webdriver) -> None:
        self._driver = driver

    def get_element(self, locator: str, timeout=10):
        by = get_locator_by_string(locator)
        return WebDriverWait(self._driver, timeout).until(
            ex_cond.visibility_of_element_located(by), ' : '.join(by))

    def get_no_element(self, locator: str, timeout=10):
        by = get_locator_by_string(locator)
        element = WebDriverWait(self._driver, timeout).until(
            ex_cond.invisibility_of_element_located(by), ' : '.join(by))
        if element is None:
            return 'No element found'

    def get_elements(self, locator: str, timeout=10):
        by = get_locator_by_string(locator)
        return WebDriverWait(self._driver, timeout).until(
            ex_cond.visibility_of_any_elements_located(by), ' : '.join(by))

    def get_element_text(self, locator: str, timeout=10):
        by = get_locator_by_string(locator)
        element = WebDriverWait(self._driver, timeout).until(
            ex_cond.visibility_of_element_located(by), ' : '.join(by))
        return element.text

    def get_element_and_click(self, locator: str, timeout=10):
        by = get_locator_by_string(locator)
        element = WebDriverWait(self._driver, timeout).until(
            ex_cond.visibility_of_element_located(by), ' : '.join(by))
        assert element.is_displayed() is True, 'Cannot press to the button'
        return element.click()

    def get_element_left_swipe(self, locator: str, timeout=10):
        by = get_locator_by_string(locator)
        element = WebDriverWait(self._driver, timeout).until(
            ex_cond.visibility_of_element_located(by), ' : '.join(by))
        left_x = element.location['x']
        right_x = left_x + element.size['width']
        upper_y = element.location['y']
        lower_y = upper_y + element.size['height']
        middle_y = (upper_y + lower_y) / 2
        self._driver.swipe(right_x, middle_y, left_x, middle_y, duration=500)