from selenite.shared.managed import browser


def page_classes(url: str = None, iframe: str = None, components: list = None):
    """
    Decorator function that adds other page classes to a page class and automatically calls self.open_url(url) when instantiated.

    :param url: The page URL.
    :param iframe: The page iframe.
    :param components: A list of page classes to be added.
    :return: A new decorator function.
    """

    def wrapper(cls):
        orig_init = cls.__init__
        orig_getattribute = cls.__getattribute__

        def new_init(self, *args, **kwargs):
            orig_init(self, *args, **kwargs)
            browser.get(url) if url else None
            browser.switch_to.frame(iframe) if iframe else None

        def new_getattribute(self, name):
            [setattr(self, component.__name__, component()) for component in components] if components else None
            return orig_getattribute(self, name)

        cls.__init__ = new_init
        cls.__getattribute__ = new_getattribute

        return cls

    return wrapper
