from typing import Union, Tuple

from selenium.webdriver.common.by import By

from selenite.ex.locator_format import check_locator_format_args


@check_locator_format_args
def s(locator: Tuple[Union[str, By], str], *args) -> Tuple[Union[str, By], str]:
    """
    使用给定的参数处理定位器。

    :param locator: Tuple[Union[str, By], str]，一个用于定位元素的 (by, value) 元组。
    :param args: 用于格式化定位器中的值的位置参数。
    :return: Tuple[Union[str, By], str]，格式化后的定位器。
    """

    # 从定位器中提取 by 类型和 value 值
    by_type, value = locator

    # 使用给定的位置参数格式化 value 值
    value = value.format(*args)

    # 结合 by 类型和格式化后的 value 值形成定位器字符串
    return by_type, value
