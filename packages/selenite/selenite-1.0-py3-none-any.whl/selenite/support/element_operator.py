import base64
from typing import Optional, Union

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from selenite.ex.element_unique import ensure_element_unique
from selenite.driver.webdriver import SeleniumDriverWrapper
from selenite.helpers.ocr_wrapper import get_img_text


class ElementOperator(SeleniumDriverWrapper):
    """
    ElementOperator 类封装了 Selenium WebDriver 对象，提供了一些常用的元素操作方法。继承自 SeleniumDriverWrapper。
    """

    def __init__(self, driver: WebDriver) -> None:
        """
        构造函数，接受一个 WebDriver 对象作为参数，并将其存储在类的 "driver" 属性中。

        :param driver: 用于操作浏览器的 WebDriver 对象。
        """
        super().__init__(driver)

    @ensure_element_unique
    def _get_element(self, element_or_locator: Union[WebElement, tuple]) -> WebElement:
        """
        从 WebElement 对象或者元组类型的定位器获取 WebElement 对象。

        :param element_or_locator: 表示元素的 WebElement 对象或者元组类型的定位器。
        :return: 表示元素的 WebElement 对象。
        """
        element = element_or_locator
        return element

    def get_text(self, element_or_locator: Union[WebElement, tuple]) -> str:
        """
        获取元素的文本内容。

        :param element_or_locator: 表示元素的 WebElement 对象或者元组类型的定位器。
        :return: 元素的文本内容。
        """
        element = self._get_element(element_or_locator)
        return element.text

    def click(self, element_or_locator: Union[WebElement, tuple]) -> None:
        """
        点击元素。

        :param element_or_locator: 表示元素的 WebElement 对象或者元组类型的定位器。
        """
        element = self._get_element(element_or_locator)
        element.click()

    def clear(self, element_or_locator: Union[WebElement, tuple]) -> None:
        """
        清除元素的内容。

        :param element_or_locator: 表示元素的 WebElement 对象或者元组类型的定位器。
        """
        element = self._get_element(element_or_locator)
        element.clear()

    def get_attribute(self, element_or_locator: Union[WebElement, tuple], attribute_name: str) -> Optional[str]:
        """
        获取元素的指定属性值。

        :param element_or_locator: 表示元素的 WebElement 对象或者元组类型的定位器。
        :param attribute_name: 要获取的属性名。
        :return: 元素的指定属性值，如果属性不存在则返回 None。
        """
        element = self._get_element(element_or_locator)
        return element.get_attribute(attribute_name)

    def send_keys(self, element_or_locator: Union[WebElement, tuple], text: str) -> None:
        """
        模拟在元素中输入文本。

        :param element_or_locator: 表示元素的 WebElement 对象或者元组类型的定位器。
        :param text: 要输入的文本。
        """
        element = self._get_element(element_or_locator)
        element.send_keys(text)

    def screenshot_as_base64(self, element_or_locator: Union[WebElement, tuple]) -> str:
        """
        对指定的 WebElement 对象进行截图并将其以 base64 编码的字符串形式返回。

        :param element_or_locator: 表示元素的 WebElement 对象或者元组类型的定位器。
        :return: 以 base64 编码的字符串表示的 WebElement 截图。
        """
        element = self._get_element(element_or_locator)
        return element.screenshot_as_base64

    def text_recognition(self, element_or_locator: Union[WebElement, tuple]) -> str:
        """
        对指定元素或定位器所对应的图片进行 OCR（光学字符识别），并返回识别出的文本。

        :param element_or_locator: 表示元素的 WebElement 对象或者元组类型的定位器。
        :return: 代表识别出文本的字符串。
        """
        image_bytes = base64.b64decode(self.screenshot_as_base64(element_or_locator))
        return get_img_text(image_bytes)
