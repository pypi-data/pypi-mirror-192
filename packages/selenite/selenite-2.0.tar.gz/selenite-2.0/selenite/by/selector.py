from typing import Tuple, Union

from selenium.webdriver.common.by import By


class BySelector:

    @staticmethod
    def id(id_: str) -> Tuple[Union[By, str], str]:
        """
        Returns a locator that matches an element with the specified ID attribute value.

        :param id_: The value of the ID attribute to match.
        :return: A tuple representing the locator.
        """
        return By.ID, id_

    @staticmethod
    def name(name_: str) -> Tuple[Union[By, str], str]:
        """
        Returns a locator that matches an element with the specified name attribute value.

        :param name_: The value of the name attribute to match.
        :return: A tuple representing the locator.
        """
        return By.NAME, name_

    @staticmethod
    def class_name(name_: str) -> Tuple[Union[By, str], str]:
        """
        Returns a locator that matches an element with the specified class name.

        :param name_: The value of the class name to match.
        :return: A tuple representing the locator.
        """
        return By.CLASS_NAME, name_

    @staticmethod
    def css(css_: str) -> Tuple[Union[By, str], str]:
        """
        Returns a locator that matches an element with the specified CSS selector.

        :param css_: The CSS selector to match.
        :return: A tuple representing the locator.
        """
        return By.CSS_SELECTOR, css_

    @staticmethod
    def xpath(xpath_: str) -> Tuple[Union[By, str], str]:
        """
        Returns a locator that matches an element with the specified XPath expression.

        :param xpath_: The XPath expression to match.
        :return: A tuple representing the locator.
        """
        return By.XPATH, xpath_

    @staticmethod
    def text(text_: str) -> Tuple[Union[By, str], str]:
        """
        Returns a locator that matches an element with the specified text content.

        :param text_: The text content to match.
        :return: A tuple representing the locator.
        """
        xpath_value = './/*[text()[normalize-space(.) = ' + BySelector._escape_text_quotes_for_xpath(text_) + ']]'
        return By.XPATH, xpath_value

    @staticmethod
    def partial_text(text_: str) -> Tuple[Union[By, str], str]:
        """
        Returns a locator that matches an element with the specified partial text content.

        :param text_: The partial text content to match.
        :return: A tuple representing the locator.
        """
        xpath_value = './/*[text()[contains(normalize-space(.), ' + BySelector._escape_text_quotes_for_xpath(
            text_) + ')]]'
        return By.XPATH, xpath_value

    @staticmethod
    def _escape_text_quotes_for_xpath(value: str) -> str:
        """
        Escapes quotes in the specified value for use in an XPath expression.

        :param value: The value to escape.
        :return: The escaped value.
        """
        return 'concat("", "%s")' % (str("\', '\"', \'".join(value.split('"'))))
