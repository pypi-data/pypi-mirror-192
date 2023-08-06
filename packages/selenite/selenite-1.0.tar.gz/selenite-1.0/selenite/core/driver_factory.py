from typing import Optional

from selenium import webdriver

from selenite.config.webdriver_config import WebDriverConfig


class DriverFactory:

    def __init__(self, config: WebDriverConfig) -> None:
        """
        构造函数，初始化 WebDriver 配置。

        :param config: 一个 WebDriverConfig 对象，包含 WebDriver 的配置选项。
        """
        self._config = config

    def _create_driver(self) -> Optional[webdriver.Chrome]:
        """
        私有方法，根据给定的配置对象创建 Chrome WebDriver 对象。

        :return: 如果配置对象有效，则返回一个 Chrome WebDriver 对象，否则返回 None。
        """
        if not isinstance(self._config, WebDriverConfig):
            return None

        options = self._config.chrome_options

        if self._config.fullscreen:
            options.add_argument("--start-maximized")
        else:
            options.add_argument(
                f"--window-size={self._config.window_size['width']},{self._config.window_size['height']}")

        if self._config.implicit_wait:
            options.add_argument(f"--implicit-wait={self._config.implicit_wait}")

        if self._config.page_load_timeout:
            options.add_argument(f"--page-load-timeout={self._config.page_load_timeout}")

        options.add_argument(f"--page-load-strategy={self._config.page_load_strategy}")

        if self._config.remote:
            return webdriver.Remote(command_executor=self._config.remote_url, options=options)
        else:
            return getattr(webdriver, self._config.browser.title())(options=options)

    @property
    def webdriver(self) -> Optional[webdriver.Chrome]:
        """
        属性方法，根据给定的配置对象创建并返回一个 Chrome WebDriver 对象。

        :return: 如果配置对象有效，则返回一个 Chrome WebDriver 对象，否则返回 None。
        """
        return self._create_driver()
