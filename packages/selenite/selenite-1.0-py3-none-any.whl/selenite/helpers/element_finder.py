from typing import Union, Tuple, List

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from selenite.helpers.deal_locator import deal_locator


def element_finder(driver_or_element: Union[WebDriver, WebElement],
                   locator: Tuple[Union[str, By], str],
                   timeout: int = 10) -> Union[WebElement, List[WebElement], None]:
    """
    根据指定的定位器获取 Web 元素。

    :param driver_or_element: Union[WebDriver, WebElement]，用于搜索元素的上下文，可以是 WebDriver 或 WebElement 对象。
    :param locator: Tuple[Union[str, By], str]，表示元素的定位器，是一个 (by, value) 的元组。
    :param timeout: Int，等待元素出现的最长时间。
    :return: Union[WebElement, List[WebElement], None]，返回找到的 Web 元素（可能是单个元素或元素列表），如果未找到，则返回 None。
    """

    by, value = deal_locator(locator)

    try:
        wait = WebDriverWait(driver_or_element, timeout)
        elements = wait.until(ec.presence_of_all_elements_located((by, value)))
        if not elements:
            return None
        elif len(elements) == 1:
            return elements[0]
        else:
            return elements
    except (NoSuchElementException, TimeoutException):
        return None
