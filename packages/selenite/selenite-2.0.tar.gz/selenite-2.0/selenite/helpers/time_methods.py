import datetime


class TimeUtils:
    """
    Utility class for dealing with time-related operations.
    """

    @staticmethod
    def get_timestamp() -> int:
        """
        Return the current Unix timestamp in seconds.

        :return: The current Unix timestamp in seconds.
        """
        return int(datetime.datetime.timestamp(datetime.datetime.now()))

    @staticmethod
    def get_utc_datetime() -> datetime.datetime:
        """
        Return the current UTC time.

        :return: The current UTC time.
        """
        return datetime.datetime.utcnow()

    @staticmethod
    def format_datetime(dt: datetime.datetime, time_format: str) -> str:
        """
        Format the given datetime object according to the specified format string.

        :param dt: The datetime object to be formatted.
        :param time_format: The format string to use for formatting the datetime object.
        :return: The formatted datetime string.
        """
        return dt.strftime(time_format)
