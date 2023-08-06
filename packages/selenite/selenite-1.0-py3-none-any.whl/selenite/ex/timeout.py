import threading


def timeout(seconds, error_message="函数调用超时"):
    """
    装饰器：如果函数运行时间超过指定的时间，则超时。

    :param seconds: 超时时间（秒）。
    :param error_message: 超时时要引发的错误信息。
    :return: 超时函数调用的包装函数。
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            """
            超时函数调用的包装函数。

            :return: 如果在超时前完成，则为原始函数调用的结果。如果函数调用超时，则返回 None。
            """

            def run():
                result = func(*args, **kwargs)
                wrapper.result = result

            t = threading.Thread(target=run)
            t.daemon = True
            t.start()
            t.join(timeout=seconds)

            if t.is_alive():
                raise TimeoutError(error_message)

            return wrapper.result if hasattr(wrapper, "result") else None

        return wrapper

    return decorator
