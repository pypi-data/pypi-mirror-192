import datetime


class TimeMethods:
    """
    时间相关的工具类，包括获取当前时间戳、UTC时间和格式化datetime对象等方法。
    """

    @staticmethod
    def get_timestamp():
        """
        返回当前时间戳的整数值。
        :return: 当前时间戳的整数值。
        """
        return int(datetime.datetime.timestamp(datetime.datetime.now()))

    @staticmethod
    def get_utc_datetime():
        """
        返回当前 UTC 时间。

        :return: 当前 UTC 时间。
        """
        return datetime.datetime.utcnow()

    @staticmethod
    def format_datetime(dt, time_format):
        """
        根据指定的格式字符串对给定的 datetime 对象进行格式化。

        :param dt: 要进行格式化的 datetime 对象。
        :param time_format: 用于格式化 datetime 对象的格式字符串。
        :return: 格式化后的 datetime 字符串。
        """
        return dt.strftime(time_format)
