from typing import Tuple, Union

from selenium.webdriver.common.by import By

from selenite.by.element import element_finder, try_check_locator_format_args
from selenite.shared.managed import browser
from selenite.support.element_j import ElementJ


def s(locator: Tuple[Union[str, By], str], *args) -> ElementJ:
    """
    Finds a web element on the page using the given locator, and returns an ElementJ object that wraps around the element.
    The locator can be a tuple of (locator type, locator value), or a ByLocator object.
    The element can also be identified with formatted string arguments.
    """

    try_check_locator_format_args(locator, *args)
    by_type, value = locator
    value = value.format(*args)
    element = ElementJ(browser, element_finder((by_type, value)).id)
    return element
