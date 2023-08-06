import time

from selenium.webdriver.remote.webdriver import WebDriver

from selenite.driver.webdriver import SeleniumDriverWrapper


class SeleniumWaitWrapper(SeleniumDriverWrapper):
    """
    一个包装类，扩展了 SeleniumDriverWrapper 类，并添加了在 Selenium 中实现等待的其他功能。
    """

    def __init__(self, driver: WebDriver):
        """
        使用 WebDriver 对象初始化 SeleniumWaitWrapper 对象。

        :param driver: WebDriver 对象。
        """
        super().__init__(driver)

    def force_sleep(self, seconds: float) -> None:
        """
        强制线程休眠给定的秒数。

        :param seconds: 要休眠的秒数。
        """
        time.sleep(seconds)
