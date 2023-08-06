import functools
import inspect
from typing import Callable

import requests
import urllib3
from requests import RequestException
from urllib3.exceptions import InsecureRequestWarning

from selenite.impl.http_methods import HTTPMethod

# 禁用 InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

# 通用请求头
COMMON_HEADERS = {
    "Content-Type": "application/json;charset=UTF-8",
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.76",
}


class Request:
    """用于进行 HTTP 请求并将响应以 JSON 格式返回的类。"""

    def __init__(self, url: str, method: str = HTTPMethod.GET) -> None:
        """
        构造函数，初始化请求的 URL 和 HTTP 方法。

        :param url: 字符串，包含要请求的 URL。
        :param method: 字符串，包含用于请求的 HTTP 方法。默认值为 "get"。
        """
        self.url = url
        self.method = method
        self.func_return = {}
        self.func_im_self = None
        self.session = None

    def __call__(self, func: Callable) -> Callable:
        """
        装饰器，将函数转换为带有给定 URL 和方法的 HTTP 请求。

        :param func: 要装饰并转换为 HTTP 请求的函数。
        :return: 装饰后的函数。
        """
        self.func = func
        self.is_class = False
        try:
            if inspect.getfullargspec(self.func).args[0] == "self":
                self.is_class = True
        except IndexError:
            pass

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self.func_return = self.func(*args, **kwargs) or {}
            self.func_im_self = args[0] if self.is_class else object
            self.create_url()
            self.create_session()
            try:
                res = requests.request(
                    self.method,
                    self.url,
                    # 解决 SSL 报错
                    verify=False,
                    **self.session
                )
                res.encoding = res.apparent_encoding
            except RequestException as e:
                raise RequestException(f"请求失败: {e}")
            else:
                return res.json()

        return wrapper

    def create_url(self) -> None:
        """
        通过将基础 URL 与端点相结合生成请求的完整 URL。
        """
        base_url = getattr(self.func_im_self, "base_url", "")
        self.url = self.func_return.pop("url", None) or self.url
        self.url = "".join([base_url, self.url])

    def create_session(self) -> None:
        """
        生成请求的会话参数，包括标头、JSON 数据、查询参数、表单数据和文件。
        """
        headers = getattr(self.func_im_self, "header", {})
        headers.update(COMMON_HEADERS)
        self.session = {
            "headers": headers,
            "json": self.func_return.pop("json", None),
            "params": self.func_return.pop("params", None),
            "data": self.func_return.pop("data", None),
            "files": self.func_return.pop("files", None),
        }
