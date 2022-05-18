"""
It is generally a good idea to define custome exceptions / errors in one's package,
vague exception handling is a recipe for trouble.
"""


class PyapidParseError(Exception):
    """
    Raised when unable to parse reqeust data.
    """


class PyapidMiscError(Exception):
    """
    Raised when an unexpected error occurs, that is not a parse error.
    """


class PyapidDBError(Exception):
    """
    Raised when there is an error communicating or querying the database.
    """
