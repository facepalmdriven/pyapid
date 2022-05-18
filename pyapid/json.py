"""
Code to parse the request data and do something useful with it.

TODO: Support for paring the request data as CSV.
TODO: Maybe add support for Pandas DataFrame and other formats as output.
"""


import json
import pyapid as api


def parse(data: str) -> any:
    """
    Default data processor for json data.
    """

    try:
        return json.loads(data)
    except json.JSONDecodeError as err:
        raise api.PyapidParseError(f"Unable to parse data: {err}")


def dump(data: any) -> str:
    """
    Dump the parsed JSON in human readable form.
    """

    try:
        return json.dumps(data, indent=2, sort_keys=True)
    except (TypeError, OverflowError, ValueError) as err:
        raise api.PyapidParseError(f"Unable to dump data: {err}")
