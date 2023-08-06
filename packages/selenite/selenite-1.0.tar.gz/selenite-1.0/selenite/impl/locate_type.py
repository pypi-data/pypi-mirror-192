from enum import Enum

from selenium.webdriver.common.by import By


class LocatorType(Enum):
    """
    枚举定位器类型，用于使用 Selenium WebDriver 确定页面上的 Web 元素。
    每个定位器类型与一个相应的 Selenium `By` 对象相关联。
    """

    ID = By.ID
    NAME = By.NAME
    CLASS_NAME = By.CLASS_NAME
    TAG_NAME = By.TAG_NAME
    LINK_TEXT = By.LINK_TEXT
    PARTIAL_LINK_TEXT = By.PARTIAL_LINK_TEXT
    CSS_SELECTOR = By.CSS_SELECTOR
    XPATH = By.XPATH
