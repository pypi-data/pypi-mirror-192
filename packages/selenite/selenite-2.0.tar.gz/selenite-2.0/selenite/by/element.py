from typing import Union, List, Tuple

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from selenite.shared.managed import browser


def element_finder(locator: Tuple[Union[str, By], str]):
    """
    A wrapper function that checks for the existence of a unique element on the page, identified using a locator tuple or a ByLocator object.
    If the element does not exist or is not unique, the function raises a ValueError exception.
    """

    element = get_element(browser, locator)
    if not element:
        raise ValueError(f'Element {locator} does not exist.')
    elif isinstance(element, list):
        raise ValueError(f'Found multiple {locator} elements. Expected only one.')
    return element


def try_check_locator_format_args(locator: Tuple[Union[str, By], str], *args) -> Tuple:
    """
    Checks the number of format arguments in the locator string matches the number of passed arguments.

    :param locator: Tuple[Union[str, By], str], the locator of the element.
    :param args: Union[str], the arguments to substitute in the locator string.
    :return: Tuple, a tuple containing the by and value parts of the locator.
    """
    by, value = locator

    count_left_braces = value.count('{')
    count_right_braces = value.count('}')
    if count_left_braces != count_right_braces:
        raise ValueError('The number of "{" and "}" in the string is not equal.')
    if count_left_braces != len(args):
        raise ValueError('The number of "{}" in the string is not equal to the number of arguments.')
    return by, value


def get_element(driver_or_element: Union[WebDriver, WebElement],
                locator: Tuple[Union[str, By], str],
                timeout: int = 10) -> Union[WebElement, List[WebElement], None]:
    """
    Find a web element based on the given locator.

    :param driver_or_element: Union[WebDriver, WebElement], the context to search the element in, can be a WebDriver or WebElement object.
    :param locator: Tuple[Union[str, By], str], the locator of the element, a tuple of (by, value).
    :param timeout: Int, the maximum time to wait for the element to appear.
    :return: Union[WebElement, List[WebElement], None], the found web element(s), which can be a single element or a list of elements. If no element is found, returns None.
    """

    by, value = locator

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
