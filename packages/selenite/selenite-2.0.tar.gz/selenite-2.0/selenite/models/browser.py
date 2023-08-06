from typing import Optional

from selenium import webdriver

from selenite.models.browser_config import BrowserConfig


class Browser:
    def __init__(self, config: BrowserConfig) -> None:
        """
        Constructor, initializes WebDriver configuration.

        :param config: A WebDriverConfig object, containing WebDriver configuration options.
        """
        self._config = config

    def _create_driver(self) -> Optional[webdriver.Chrome]:
        """
        Private method, creates a Chrome WebDriver object based on the given configuration object.

        :return: A Chrome WebDriver object if the configuration object is valid, otherwise None.
        """
        if not isinstance(self._config, BrowserConfig):
            return None

        options = self._config.chrome_options

        if self._config.fullscreen:
            options.add_argument('--start-maximized')
        else:
            options.add_argument(
                f'--window-size={self._config.window_size["width"]},{self._config.window_size["height"]}')

        if self._config.implicit_wait:
            options.add_argument(f'--implicit-wait={self._config.implicit_wait}')

        if self._config.page_load_timeout:
            options.add_argument(f'--page-load-timeout={self._config.page_load_timeout}')

        options.add_argument(f'--page-load-strategy={self._config.page_load_strategy}')

        if self._config.remote:
            return webdriver.Remote(command_executor=self._config.remote_url, options=options)
        else:
            return getattr(webdriver, self._config.browser.title())(options=options)

    @property
    def webdriver(self) -> Optional[webdriver.Chrome]:
        """
        Property method, creates and returns a Chrome WebDriver object based on the given configuration object.

        :return: A Chrome WebDriver object if the configuration object is valid, otherwise None.
        """
        return self._create_driver()
