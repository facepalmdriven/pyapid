"""
It is generally a good idea to define custome exceptions / errors in one's package,
vague exception handling is a recipe for trouble.

To avoid circular imports it is also useuful to define types separately too, so they can
be imported everywhere they are needed.
"""

from datetime import date, datetime

from pydantic import BaseModel, validator


class Data(BaseModel):
    stock: str
    start: date
    end: date

    @staticmethod
    def parse_date(str_date: str) -> datetime:
        return datetime.strptime(str_date, "%Y-%m-%d").date()

    @validator("start", pre=True)
    @classmethod
    def parse_start_date(cls, value: str) -> datetime:
        return Data.parse_date(value)

    @validator("end", pre=True)
    @classmethod
    def parse_end_date(cls, value: str) -> datetime:
        return Data.parse_date(value)


# TODO: If doing more work in reports you will likely need to raise custom exceptions,
#   in that case use something like these.
#
class PyapidParseError(Exception):
    """
    Raised when unable to parse reqeust data.
    """


# class PyapidMiscError(Exception):
#     """
#     Raised when an unexpected error occurs, that is not a parse error.
#     """

# class PyapidDBError(Exception):
#     """
#     Raised when there is an error communicating or querying the database.
#     """
