from selenite.config.webdriver_config import WebDriverConfig

# 创建一个 WebDriverConfig 对象，并设置其属性以配置 WebDriver。
config = WebDriverConfig()

# 设置要使用的浏览器类型。
config.browser = "chrome"

# 设置是否使用全屏模式。
config.fullscreen = True

# 设置浏览器窗口的大小。
config.window_size = {"width": 1920, "height": 1080}

# 设置是否使用远程 WebDriver。
config.remote = False

# 设置远程 WebDriver 服务器的 URL。
config.remote_url = "http://192.168.15.92:5444/wd/hub"

# 设置查找元素的等待时间。
config.implicit_wait = 10

# 设置页面加载的超时时间。
config.page_load_timeout = 30

# 向 ChromeOptions 对象添加命令行参数。
# config.add_argument("--headless")
config.add_argument("--disable-gpu")
config.add_argument("--disable-infobars")
config.add_argument("--hide-scrollbars")
config.add_argument("--ignore-certificate-errors")

# 向 ChromeOptions 对象添加实验选项。
config.add_experimental_option("useAutomationExtension", False)
config.add_experimental_option("excludeSwitches", ["enable-automation"])

# 设置页面加载策略为等待页面加载完成。
config.page_load_strategy = "none"
