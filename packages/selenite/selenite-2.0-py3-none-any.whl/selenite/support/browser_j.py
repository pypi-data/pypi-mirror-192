from selenium.webdriver.remote.webdriver import WebDriver


class BaseDriver:
    """
    Encapsulates a Selenium WebDriver object and provides some commonly used operation methods for reuse throughout
    the project.
    """

    def __init__(self, driver: WebDriver) -> None:
        """
        Constructor that accepts a WebDriver object as a parameter and stores it in the class's "driver" attribute.

        :param driver: The WebDriver object used to manipulate the browser.
        """
        self.driver = driver
