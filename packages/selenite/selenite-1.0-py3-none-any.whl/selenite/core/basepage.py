from selenite.support.browser_driver import BrowserDriver
from selenite.support.ec_wrapper import SeleniumECWrapper
from selenite.support.element_operator import ElementOperator
from selenite.support.wait_wrapper import SeleniumWaitWrapper


class BasePage(BrowserDriver, ElementOperator, SeleniumECWrapper, SeleniumWaitWrapper):
    """
    BasePage 类是一个页面对象模型（Page Object Model）的基类，封装了常用的 WebDriver 操作方法和一些常用的
    Expected Conditions 和等待方法。

    BasePage 类继承自 BrowserDriver、ElementOperator、SeleniumECWrapper 和 SeleniumWaitWrapper。
    """
    pass
