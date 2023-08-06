from selenium.webdriver.common.by import By


class LocatorType:
    """
    Constants class for defining locator types for use with Selenium WebDriver to identify Web elements on a page.
    Each type of locator is associated with a corresponding Selenium `By` object.
    """

    # The element's identifier (id).
    ID = By.ID

    # The element's name attribute.
    NAME = By.NAME

    # The element's class name.
    CLASS_NAME = By.CLASS_NAME

    # The element's tag name.
    TAG_NAME = By.TAG_NAME

    # The element's link text.
    LINK_TEXT = By.LINK_TEXT

    # The element's partial link text.
    PARTIAL_LINK_TEXT = By.PARTIAL_LINK_TEXT

    # The element's CSS selector.
    CSS_SELECTOR = By.CSS_SELECTOR

    # The element's XPath expression.
    XPATH = By.XPATH
