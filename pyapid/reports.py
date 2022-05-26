"""
Logic to do something with parsed data
"""

import yfinance as yf

import pyapid.database as db
from pyapid.types import Data, PyapidParseError


def fetch_data(d: Data) -> dict:
    """
    Get data for the report.

    Raises PyapidParseError if unable to parse data or if data is not available.
    """

    # This results in a Pandas DataFrame
    ticker = yf.download(
        d.stock, start=d.start, end=d.end, progress=False, show_errors=False
    )

    if ticker.empty:
        raise PyapidParseError("Could not get the data based on the query")

    timestamps = []
    data = []

    for t, r in ticker.iterrows():
        timestamps.append(t.timestamp())
        data.append(r.to_json())

    return (timestamps, data)


def create(d: Data) -> list[dict]:
    """
    Generate a new report.

    TODO: Validate data, f.e. since we are returning Close here, probably should not
    query if current day is included, since Close has not been reached yet. Times are
    checked by the Data class.
    """

    try:
        timestamps, data = fetch_data(d)
    except PyapidParseError:
        raise

    return db.insert(d.stock, d.start, d.end, [timestamps, data])


def get(uuid=None) -> dict:
    """
    Get the specific report, or all of them.
    """

    return db.select(uuid)
