from typing import Any


dt_to_regexp_format_specifiers = {
    "%a": r"\w{3}",  # abbreviated weekday name
    "%A": r"\w+",  # full weekday name
    "%w": r"[0-6]",  # weekday as a decimal number, where 0 is Sunday and 6 is Saturday
    "%d": r"\d{2}",  # day of the month as a zero-padded decimal number
    "%b": r"\w{3}",  # abbreviated month name
    "%B": r"\w+",  # full month name
    "%m": r"\d{2}",  # month as a zero-padded decimal number
    "%y": r"\d{2}",  # year without century as a decimal number
    "%Y": r"\d{4}",  # year with century as a decimal number
    "%H": r"\d{2}",  # hour (24-hour clock) as a zero-padded decimal number
    "%I": r"\d{2}",  # hour (12-hour clock) as a zero-padded decimal number
    "%p": r"AM|PM",  # either AM or PM
    "%M": r"\d{2}",  # minute as a zero-padded decimal number
    "%S": r"\d{2}",  # second as a zero-padded decimal number
    "%f": r"\d{6}",  # microsecond as a decimal number, zero-padded on the left
    "%z": r"[+-]\d{4}",  # UTC offset in the form +HHMM or -HHMM
    "%Z": r"\w+",  # time zone name
    "%j": r"\d{3}",  # day of the year as a zero-padded decimal number
    "%U": r"\d{2}",  # week number of the year (Sunday as the first day of the week) as a zero-padded decimal number
    "%W": r"\d{2}",  # week number of the year (Monday as the first day of the week) as a zero-padded decimal number
    "%c": r".+",  # appropriate date and time representation
    "%x": r".+",  # appropriate date representation
    "%X": r".+",  # appropriate time representation
    "%G": r"\d{4}",  # the ISO 8601 year with century as a decimal number.
    "%u": r"[1-7]",  # weekday as a decimal number [1, 7], with 1 representing Monday.
    "%V": r"\d{2}",  # ISO week number, with Monday as the first day of the week
}


dt_to_human_format_specifiers = {
    "%a": "ddd",  # abbreviated weekday name
    "%A": "dddd",  # full weekday name
    "%w": "d",  # weekday as a decimal number, where 0 is Sunday and 6 is Saturday
    "%d": "dd",  # day of the month as a zero-padded decimal number
    "%b": "MMM",  # abbreviated month name
    "%B": "MMMM",  # full month name
    "%m": "MM",  # month as a zero-padded decimal number
    "%y": "yy",  # year without century as a decimal number
    "%Y": "yyyy",  # year with century as a decimal number
    "%H": "HH",  # hour (24-hour clock) as a zero-padded decimal number
    "%I": "hh",  # hour (12-hour clock) as a zero-padded decimal number
    "%p": "AM/PM",  # either AM or PM
    "%M": "mm",  # minute as a zero-padded decimal number
    "%S": "ss",  # second as a zero-padded decimal number
    "%f": "ffffff",  # microsecond as a decimal number, zero-padded on the left
    "%z": "ZZ",  # UTC offset in the form +HHMM or -HHMM
    "%Z": "z",  # time zone name
    "%j": "DDD",  # day of the year as a zero-padded decimal number
    "%U": "ww",  # week number of the year (Sunday as the first day of the week) as a zero-padded decimal number
    "%W": "WW",  # week number of the year (Monday as the first day of the week) as a zero-padded decimal number
    "%c": "ccc",  # appropriate date and time representation
    "%x": "cx",  # appropriate date representation
    "%X": "cX",  # appropriate time representation
    "%G": "YYYY",  # the ISO 8601 year with century as a decimal number.
    "%u": "u",  # weekday as a decimal number [1, 7], with 1 representing Monday.
    "%V": "VV",  # ISO week number, with Monday as the first day of the week
}


def from_dt_f_to_regexp(fmt: str) -> str:
    """
    Generate from datetime format string to datetime validation regexp
    "%Y-%m-%d" -> "^$|^[0-9]{4}-[0-9]{2}-[0-9]{2}$"

    Args:
        fmt (str): "%Y-%m-%d"

    Returns:
        str: "^$|^[0-9]{4}-[0-9]{2}-[0-9]{2}$"
    """
    for specifier, specifier_regexp in dt_to_regexp_format_specifiers:
        fmt = fmt.replace(specifier, specifier_regexp)
    return "^$|^" + fmt + "$"


def from_dt_f_to_human(fmt: str) -> str:
    """
    Generate from datetime format string to human-reading format
    "%Y-%m-%d" -> "YYYY-mm-dd"

    Args:
        fmt (str): "%Y-%m-%d"

    Returns:
        str: "YYYY-mm-dd"
    """
    for specifier, specifier_regexp in dt_to_human_format_specifiers:
        fmt = fmt.replace(specifier, specifier_regexp)
    return fmt


def access_dict_key_or_create(d: dict, key: Any, default_value: Any) -> Any:
    if key in d.keys():
        return d[key]
    d[key] = default_value
    return d[key]
