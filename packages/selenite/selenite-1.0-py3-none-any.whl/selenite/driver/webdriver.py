from selenium.webdriver.remote.webdriver import WebDriver


class SeleniumDriverWrapper:
    """
    封装了一个 Selenium WebDriver 对象并提供了一些常用的操作方法以便在整个项目中重用。
    """

    def __init__(self, driver: WebDriver) -> None:
        """
        构造函数，接受一个 WebDriver 对象作为参数，并将其存储在类的 "driver" 属性中。

        :param driver: 用于操作浏览器的 WebDriver 对象。
        """
        self.driver = driver
