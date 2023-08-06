from typing import Tuple, Union

from selenium.webdriver.common.by import By


class BySelector:

    @staticmethod
    def id(id_: str) -> Tuple[Union[By, str], str]:
        """
        返回一个匹配具有指定 ID 的元素的定位器。

        :param id_: 要匹配的 ID 属性的值。
        :return: 表示定位器的元组。
        """
        return By.ID, id_

    @staticmethod
    def name(name_: str) -> Tuple[Union[By, str], str]:
        """
        返回一个匹配具有指定名称属性的元素的定位器。

        :param name_: 要匹配的名称属性的值。
        :return: 表示定位器的元组。
        """
        return By.NAME, name_

    @staticmethod
    def class_name(name_: str) -> Tuple[Union[By, str], str]:
        """
        返回一个匹配具有指定类名的元素的定位器。

        :param name_: 要匹配的类名的值。
        :return: 表示定位器的元组。
        """
        return By.CLASS_NAME, name_

    @staticmethod
    def css(css_: str) -> Tuple[Union[By, str], str]:
        """
        返回一个匹配具有指定 CSS 选择器的元素的定位器。

        :param css_: 要匹配的 CSS 选择器。
        :return: 表示定位器的元组。
        """
        return By.CSS_SELECTOR, css_

    @staticmethod
    def xpath(xpath_: str) -> Tuple[Union[By, str], str]:
        """
        返回一个匹配具有指定 XPath 表达式的元素的定位器。

        :param xpath_: 要匹配的 XPath 表达式。
        :return: 表示定位器的元组。
        """
        return By.XPATH, xpath_

    @staticmethod
    def text(text_: str) -> Tuple[Union[By, str], str]:
        """
        返回一个匹配具有指定文本内容的元素的定位器。

        :param text_: 要匹配的文本内容。
        :return: 表示定位器的元组。
        """
        xpath_value = ".//*[text()[normalize-space(.) = " + BySelector._escape_text_quotes_for_xpath(text_) + ']]'
        return By.XPATH, xpath_value

    @staticmethod
    def partial_text(text_: str) -> Tuple[Union[By, str], str]:
        """
        返回一个匹配具有指定部分文本内容的元素的定位器。

        :param text_: 要匹配的部分文本内容。
        :return: 表示定位器的元组。
        """
        xpath_value = ".//*[text()[contains(normalize-space(.), " + BySelector._escape_text_quotes_for_xpath(
            text_) + ")]]"
        return By.XPATH, xpath_value

    @staticmethod
    def _escape_text_quotes_for_xpath(value: str) -> str:
        """
        为在 XPath 表达式中使用而转义指定值中的引号。

        :param value: 要转义的值。
        :return: 转义后的值。
        """
        return 'concat("", "%s")' % (str("\", '\"', \"".join(value.split('"'))))
