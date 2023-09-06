import random
import time

from selenium.common import UnexpectedAlertPresentException

from locators.alerts_frame_windows_locators import (
    BrowserWindowsPageLocators,
    AlertsPageLocators,
    FramesPageLocators, NestedFramesPageLocators,
)
from pages.base_page import BasePage


class BrowserWindowsPage(BasePage):
    locators = BrowserWindowsPageLocators()

    def check_opened(self, open_value):
        value = {
            "tab": self.locators.NEW_TAB_BUTTON,
            "window": self.locators.NEW_WINDOW_BUTTON,
        }
        self.element_is_visible(value[open_value]).click()
        time.sleep(10)
        self.switch_to_window(1)
        text_title = self.element_is_present(self.locators.TITLE_NEW).text
        return text_title


class AlertsPage(BasePage):
    locators = AlertsPageLocators()

    def check_see_alert(self):
        self.element_is_visible(self.locators.SEE_ALERT_BUTTON).click()
        alert_window = self.driver.switch_to.alert
        return alert_window.text

    def check_alert_appear_5_sec(self):
        self.element_is_visible(self.locators.APPEAR_ALERT_AFTER_5_SEC_BUTTON).click()
        time.sleep(6)
        try:
            alert_window = self.driver.switch_to.alert
            return alert_window.text
        except UnexpectedAlertPresentException:
            alert_window = self.driver.switch_to.alert
            return alert_window.text

    def check_confirm_alert(self):
        self.element_is_visible(self.locators.CONFIRM_BOX_ALERT_BUTTON).click()
        alert_window = self.driver.switch_to.alert
        alert_window.accept()
        text_result = self.element_is_present(self.locators.CONFIRM_RESULT).text
        return text_result

    def check_prompt_alert(self):
        text = f"autotest{random.randint(0, 999)}"
        self.element_is_visible(self.locators.PROMPT_BOX_ALERT_BUTTON).click()
        alert_window = self.driver.switch_to.alert
        alert_window.send_keys(text)
        alert_window.accept()
        text_result = self.element_is_present(self.locators.PROMPT_RESULT).text
        return text, text_result


class FramesPage(BasePage):
    locators = FramesPageLocators()

    def check_frame(self, frame_num):
        frame_value = {
            "frame1": self.locators.FIRST_FRAME,
            "frame2": self.locators.SECOND_FRAME,
        }
        frame = self.element_is_present(frame_value[frame_num])
        width = frame.get_attribute("width")
        height = frame.get_attribute("height")
        self.driver.switch_to.frame(frame)
        text = self.element_is_present(self.locators.TITLE_FRAME).text
        self.driver.switch_to.default_content()
        return [text, width, height]


class NestedFramesPage(BasePage):
    locators = NestedFramesPageLocators()

    def check_nested_frame(self):
        parent_frame = self.element_is_present(self.locators.PARENT_FRAME)
        self.driver.switch_to.frame(parent_frame)
        parent_text = self.element_is_present(self.locators.PARENT_TEXT).text
        child_frame = self.element_is_present(self.locators.CHILD_FRAME)
        self.driver.switch_to.frame(child_frame)
        child_text = self.element_is_present(self.locators.CHILD_TEXT).text
        return parent_text, child_text

