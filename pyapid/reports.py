"""
Logic to do something with parsed data
"""

import yfinance as yf

import pyapid.database as db
from pyapid.types import Data, PyapidParseError


def fetch_data(data: Data) -> dict:
    """
    Get data for the report.

    Raises PyapidParseError if unable to parse data or if data is not available.
    """

    # This results in a Pandas DataFrame
    ticker = yf.download(
        data.stock, start=data.start, end=data.end, progress=False, show_errors=False
    )

    if ticker.empty:
        raise PyapidParseError("Could not get the data based on the query")

    return tuple(list(res) for res in zip(*ticker.iterrows()))


def create(data: Data) -> list[dict]:
    """
    Generate a new report.

    TODO: Validate data, f.e. since we are returning Close here, probably should not
    query if current day is included, since Close has not been reached yet. Times are
    checked by the Data class.
    """

    timestamps, data = fetch_data(data)

    return db.insert(data.stock, data.start, data.end, [timestamps, data])


def get(uuid=None) -> dict:
    """
    Get the specific report, or all of them.
    """

    return db.select(uuid)
