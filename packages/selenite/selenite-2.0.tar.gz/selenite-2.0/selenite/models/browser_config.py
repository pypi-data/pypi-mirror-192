from typing import Union, List

from selenium import webdriver

from selenite.constants.browser_type import BrowserType


class BrowserConfig:
    """
    A class for configuring WebDriver options.
    """

    def __init__(self) -> None:
        """
        Constructor that initializes the default values of WebDriver options.
        """
        self._browser = BrowserType.CHROME
        self._fullscreen = False
        self._window_size = {'width': 1920, 'height': 1080}
        self._remote = False
        self._remote_url = 'http://127.0.0.1:4444/wd/hub'
        self._implicit_wait = 10
        self._page_load_timeout = 30
        self._chrome_options = webdriver.ChromeOptions()
        self._page_load_strategy = 'normal'

    @property
    def browser(self) -> str:
        """
        Get the browser type.
        """
        return self._browser

    @browser.setter
    def browser(self, browser: str) -> None:
        """
        Set the browser type.
        """
        self._browser = browser

    @property
    def fullscreen(self) -> bool:
        """
        Get whether to use full-screen mode.
        """
        return self._fullscreen

    @fullscreen.setter
    def fullscreen(self, value: bool) -> None:
        """
        Set whether to use full-screen mode.
        """
        self._fullscreen = value

    @property
    def window_size(self) -> dict:
        """
        Get the size of the browser window.
        """
        return self._window_size

    @window_size.setter
    def window_size(self, size: dict) -> None:
        """
        Set the size of the browser window.
        """
        self._window_size = size

    @property
    def remote(self) -> bool:
        """
        Get whether to use a remote WebDriver.
        """
        return self._remote

    @remote.setter
    def remote(self, value: bool) -> None:
        """
        Set whether to use a remote WebDriver.
        """
        self._remote = value

    @property
    def remote_url(self) -> str:
        """
        Get the URL of the remote WebDriver server.
        """
        return self._remote_url

    @remote_url.setter
    def remote_url(self, value: str) -> None:
        """
        Set the URL of the remote WebDriver server.
        """
        self._remote_url = value

    @property
    def implicit_wait(self) -> int:
        """
        Get the maximum amount of time to wait for an element to appear.
        """
        return self._implicit_wait

    @implicit_wait.setter
    def implicit_wait(self, value: int) -> None:
        """
        Set the maximum amount of time to wait for an element to appear.
        """
        self._implicit_wait = value

    @property
    def page_load_timeout(self) -> int:
        """
        Get the maximum amount of time to wait for a page to load.
        """
        return self._page_load_timeout

    @page_load_timeout.setter
    def page_load_timeout(self, value: int) -> None:
        """
        Set the maximum amount of time to wait for a page to load.
        """
        self._page_load_timeout = value

    @property
    def chrome_options(self) -> webdriver.ChromeOptions:
        """
        Get the ChromeOptions object used to configure ChromeDriver.
        """
        return self._chrome_options

    def add_argument(self, arg: str) -> None:
        """
        Add a command-line argument to the ChromeOptions object.
        """
        self._chrome_options.add_argument(arg)

    def add_experimental_option(self, key: str, value: Union[str, int, dict, List[str]]) -> None:
        """
        Add an experimental option to the ChromeOptions object.
        """
        self._chrome_options.add_experimental_option(key, value)

    @property
    def page_load_strategy(self) -> str:
        """
        Get the current page load strategy.
        """
        return self._page_load_strategy

    @page_load_strategy.setter
    def page_load_strategy(self, strategy: str) -> None:
        """
        Set the page load strategy that the driver should use.
        """
        self._page_load_strategy = strategy
