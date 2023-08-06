from typing import Union, List

from selenium import webdriver

from selenite.impl.browser_type import BrowserType


class WebDriverConfig:
    """
    用于配置 WebDriver 选项的类。
    """

    def __init__(self) -> None:
        """
        构造函数，初始化 WebDriver 选项的默认值。
        """
        self._browser = BrowserType.CHROME
        self._fullscreen = False
        self._window_size = {"width": 1920, "height": 1080}
        self._remote = False
        self._remote_url = "http://127.0.0.1:4444/wd/hub"
        self._implicit_wait = 10
        self._page_load_timeout = 30
        self._chrome_options = webdriver.ChromeOptions()
        self._page_load_strategy = "normal"

    @property
    def browser(self) -> str:
        """
        获取浏览器类型。
        """
        return self._browser

    @browser.setter
    def browser(self, browser: str) -> None:
        """
        设置浏览器类型。
        """
        self._browser = browser

    @property
    def fullscreen(self) -> bool:
        """
        获取是否使用全屏模式。
        """
        return self._fullscreen

    @fullscreen.setter
    def fullscreen(self, value: bool) -> None:
        """
        设置是否使用全屏模式。
        """
        self._fullscreen = value

    @property
    def window_size(self) -> dict:
        """
        获取浏览器窗口的尺寸。
        """
        return self._window_size

    @window_size.setter
    def window_size(self, size: dict) -> None:
        """
        设置浏览器窗口的尺寸。
        """
        self._window_size = size

    @property
    def remote(self) -> bool:
        """
        获取是否使用远程 WebDriver。
        """
        return self._remote

    @remote.setter
    def remote(self, value: bool) -> None:
        """
        设置是否使用远程 WebDriver。
        """
        self._remote = value

    @property
    def remote_url(self) -> str:
        """
        获取远程 WebDriver 服务器的 URL。
        """
        return self._remote_url

    @remote_url.setter
    def remote_url(self, value: str) -> None:
        """
        设置远程 WebDriver 服务器的 URL。
        """
        self._remote_url = value

    @property
    def implicit_wait(self) -> int:
        """
        获取等待元素出现的最长时间。
        """
        return self._implicit_wait

    @implicit_wait.setter
    def implicit_wait(self, value: int) -> None:
        """
        设置等待元素出现的最长时间。
        """
        self._implicit_wait = value

    @property
    def page_load_timeout(self) -> int:
        """
        获取等待页面加载的最长时间。
        """
        return self._page_load_timeout

    @page_load_timeout.setter
    def page_load_timeout(self, value: int) -> None:
        """
        设置等待页面加载的最长时间。
        """
        self._page_load_timeout = value

    @property
    def chrome_options(self) -> webdriver.ChromeOptions:
        """
        获取用于配置 ChromeDriver 的 ChromeOptions 对象。
        """
        return self._chrome_options

    def add_argument(self, arg: str) -> None:
        """
        添加一个命令行参数到 ChromeOptions 对象中。
        """
        self._chrome_options.add_argument(arg)

    def add_experimental_option(self, key: str, value: Union[str, int, dict, List[str]]) -> None:
        """
        向 ChromeOptions 对象中添加一个实验性选项。
        """
        self._chrome_options.add_experimental_option(key, value)

    @property
    def page_load_strategy(self) -> str:
        """
        获取当前的页面加载策略。
        """
        return self._page_load_strategy

    @page_load_strategy.setter
    def page_load_strategy(self, strategy: str) -> None:
        """
        设置驱动程序要使用的页面加载策略。
        """
        self._page_load_strategy = strategy
