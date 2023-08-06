from typing import Optional

from selenium.webdriver.remote.webdriver import WebDriver

from selenite.driver.webdriver import SeleniumDriverWrapper


class BrowserDriver(SeleniumDriverWrapper):
    """
    封装了 Selenium WebDriver 对象，并提供了一些常用的浏览器操作方法。继承自 SeleniumDriverWrapper。
    """

    def __init__(self, driver: WebDriver) -> None:
        """
        构造函数，接受一个 WebDriver 对象作为参数，并将其存储在类的 "driver" 属性中。

        :param driver: 用于操作浏览器的 WebDriver 对象。
        """
        super().__init__(driver)

    def open_url(self, url: str) -> None:
        """
        打开指定 URL 的网页。

        :param url: 要打开的网页的 URL。
        """
        self.driver.get(url)

    def refresh_browser(self) -> None:
        """
        刷新当前浏览器窗口。
        """
        self.driver.refresh()

    def switch_to_frame(self, frame_reference: Optional[str] = None) -> None:
        """
        将驱动程序的焦点切换到当前页面上的一个 frame 或 iframe。

        :param frame_reference: 要切换到的 frame 的名称、ID 或 WebElement 对象。
        如果未指定，则驱动程序的焦点将设置为默认内容。
        """
        if frame_reference is None:
            self.driver.switch_to.default_content()
        else:
            self.driver.switch_to.frame(frame_reference)
