from selenite.models.browser import Browser
from selenite.models.browser_config import BrowserConfig

# Create a BrowserConfig object and set its properties to configure the WebDriver.
config = BrowserConfig()

# Set the browser type to use.
config.browser = 'chrome'

# Set whether to use fullscreen mode.
config.fullscreen = True

# Set the size of the browser window.
config.window_size = {'width': 1920, 'height': 1080}

# Set whether to use a remote WebDriver.
config.remote = False

# Set the URL of the remote WebDriver server.
config.remote_url = 'http://192.168.15.92:5444/wd/hub'

# Set the maximum time to wait for an element to appear.
config.implicit_wait = 10

# Set the maximum time to wait for a page to load.
config.page_load_timeout = 30

# Add command-line arguments to the ChromeOptions object.
# config.add_argument('--headless')
config.add_argument('--disable-gpu')
config.add_argument('--disable-infobars')
config.add_argument('--hide-scrollbars')
config.add_argument('--ignore-certificate-errors')

# Add experimental options to the ChromeOptions object.
config.add_experimental_option('useAutomationExtension', False)
config.add_experimental_option('excludeSwitches', ['enable-automation'])

# Set the page load strategy to wait for the page to finish loading.
config.page_load_strategy = 'none'

# Create a Browser object with the given configuration, and get a WebDriver object.
driver = Browser(config)
browser = driver.webdriver
