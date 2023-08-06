from selenite.helpers.deal_locator import deal_locator


def check_locator_format_args(func):
    """
    一个检查字符串中 "{}" 数量是否等于参数数量的装饰器函数。
    """

    def wrapper(locator, *args):
        """
        执行检查的内部包装函数。
        """

        by, string = deal_locator(locator)

        count_left_braces = string.count("{")
        count_right_braces = string.count("}")
        if count_left_braces != count_right_braces:
            raise ValueError("字符串中 '{' 和 '}' 的数量不相等。")
        if count_left_braces != len(args):
            raise ValueError("字符串中的 '{}' 数量和参数数量不相等。")
        return func(locator, *args)

    return wrapper
