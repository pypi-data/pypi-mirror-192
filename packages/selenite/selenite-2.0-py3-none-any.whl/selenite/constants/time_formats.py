class TimeFormats:
    """Different date and time formats."""

    # Datetime format with year, month, day, hour, minute, and second.
    DATETIME_FULL = '%Y-%m-%d %H:%M:%S'

    # Datetime format with year, month, day, hour, and minute.
    DATETIME_SHORT = '%Y-%m-%d %H:%M'

    # Datetime format with year, month, and day.
    DATETIME_DATE = '%Y-%m-%d'

    # Datetime format with hour, minute, and second.
    DATETIME_TIME = '%H:%M:%S'

    # Datetime format in UTC with year, month, day, hour, minute, and second.
    UTC_DATETIME = '%Y-%m-%dT%H:%M:%S.000Z'
