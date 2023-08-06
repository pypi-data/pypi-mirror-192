from typing import Union, Tuple

from selenium.webdriver.common.by import By

from selenite.helpers.element_finder import element_finder


def ensure_element_unique(func):
    """
    装饰器函数，确保页面上唯一的元素存在，使用定位器元组或ByLocator对象进行识别。
    如果元素不存在或不唯一，装饰器会引发ValueError异常。
    """

    def wrapper(page_obj, locator: Tuple[Union[str, By], str], *args, **kwargs):
        """
        包装函数，检查页面上唯一的元素是否存在，使用定位器元组或ByLocator对象进行识别。
        如果元素不存在或不唯一，函数会引发ValueError异常。
        """

        element = element_finder(page_obj.driver, locator)
        if not element:
            raise ValueError(f"元素 {locator} 不存在。")
        elif isinstance(element, list):
            raise ValueError(f"找到多个 {locator} 元素。只期望找到一个。")
        return func(page_obj, element, *args, **kwargs)

    return wrapper
