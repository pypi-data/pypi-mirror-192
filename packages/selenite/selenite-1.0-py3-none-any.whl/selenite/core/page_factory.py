def page_classes(url: str = None, iframe: str = None, components: list = None):
    """
    装饰器函数，用于将其他页面类添加到一个页面类中，并在实例化时自动调用 self.open_url(url)。

    :param url: 页面 URL
    :param iframe: 页面 iframe
    :param components: 要添加的页面类列表
    :return: 新的装饰器函数
    """

    def wrapper(cls):
        orig_init = cls.__init__
        orig_getattribute = cls.__getattribute__

        def new_init(self, *args, **kwargs):
            orig_init(self, *args, **kwargs)
            self.open_url(url) if url else None
            self.switch_to_frame(iframe) if iframe else None

        def new_getattribute(self, name):
            [setattr(self, component.__name__, component(self)) for component in components] if components else None
            return orig_getattribute(self, name)

        cls.__init__ = new_init
        cls.__getattribute__ = new_getattribute

        return cls

    return wrapper
