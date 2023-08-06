from typing import Tuple, Union

from selenium.webdriver.common.by import By

from selenite.impl.locate_type import LocatorType


def deal_locator(locator: Tuple[Union[str, By], str]) -> Tuple[str, str]:
    """
    将定位器元组转换为一对 (by, value) 字符串。
    元组的第一个元素应该是字符串或 By 类的成员，表示定位方法。
    元组的第二个元素应该是一个字符串，表示定位值。
    如果定位器元组无效或不支持定位方法，则引发 ValueError。

    :param locator: Tuple[Union[str, By], str], 要转换的定位器元组。
    :return: Tuple[str, str], 表示定位方法和定位值的一对 (by, value) 字符串。
    """

    if not isinstance(locator, tuple):
        raise ValueError(f"无效的定位器: {locator}。预期是 (by, value) 的元组。")
    if len(locator) != 2:
        raise ValueError(f"无效的定位器元组: {locator}。预期是长度为 2 的元组。")

    by, value = locator

    if not isinstance(by, (str, By)):
        raise ValueError(f"无效的定位器类型: {type(by)}。预期是字符串或 By 类的成员。")

    if not isinstance(value, str):
        raise ValueError(f"无效的定位值: {value}。预期是字符串。")

    by_methods = [locator_type.value for locator_type in LocatorType]
    if by not in by_methods:
        raise ValueError(f"不支持的定位方法: {by}。预期是 {by_methods} 中的一种。")

    return by, value
