import selenium.webdriver.support.expected_conditions as ec
from selenium.common import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver

from selenite.driver.webdriver import SeleniumDriverWrapper


class SeleniumECWrapper(SeleniumDriverWrapper):
    """
    将 Selenium WebDriver 包装在一个额外的 Expected Conditions 功能类中的类。
    """

    def __init__(self, driver: WebDriver) -> None:
        """
        构造函数，用 WebDriver 实例初始化一个 SeleniumECWrapper 对象。

        :param driver: 要包装的 WebDriver 对象。
        """
        super().__init__(driver)

    def verify_visibility_of_element_located(self, locator: tuple) -> bool:
        """
        验证由定位器指定的元素是否可见。

        :param locator: 包含定位器策略和定位器值的元组。
        :return: 如果元素可见，则返回 True；否则返回 False。
        """
        try:
            ec.visibility_of_element_located(locator)(self.driver)
            return True
        except NoSuchElementException:
            return False
