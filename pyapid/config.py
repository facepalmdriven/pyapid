"""
Read configuration from environment.
"""

from functools import cache
from os import getenv


class Config:
    """
    Get values from environment variables, or use defaults.
    """

    default_db = ":memory:"
    default_debug = False

    def __init__(self):
        self.db: str = getenv("PYAPID_DB", Config.default_db)
        self.debug: bool = bool(getenv("PYAPID_DEBUG", Config.default_debug))


@cache
def config():
    """
    Wrapper for Config.
    """

    return Config()
