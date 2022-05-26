import datetime
import json
from unittest.mock import patch

import pyapid.config as cfg
import pyapid.database as db
import pytest
from pyapid.types import Data
from pydantic import ValidationError


def test_config():
    """
    Verify that configuration works, both defaults and overrides from the environment
    """

    with patch.dict("os.environ", {"PYAPID_DB": "test.db"}):
        assert cfg.Config().db == "test.db"

    with patch.dict("os.environ", {"PYAPID_DEBUG": "True"}):
        assert cfg.Config().debug is True


def test_types():
    """
    Check that the Data is properly initialized and validated
    """

    data = Data(stock="avgo", start="2020-01-01", end="2020-01-02")

    assert data.stock == "avgo"
    assert data.start == datetime.date(2020, 1, 1)
    assert data.end == datetime.date(2020, 1, 2)

    with pytest.raises(ValidationError):
        Data(stock=datetime.date(2020, 1, 1), start="2020-01-01", end="2020-01-02")

    with pytest.raises(ValidationError):
        Data(stock="avgo", start="2020/01-01", end="2020-01-02")

    with pytest.raises(ValidationError):
        Data(stock="avgo", start="2020-01-01", end="2020/01-02")


@patch("pyapid.database.uuid4", return_value="1234")
def test_db(tmpdir):
    """
    Verify all database methods in one shot, as insert calls both init and select

    NOTE: uuid4 is patched inside database module, not inside stdlib!
    """
    tmp_file = str(tmpdir.join("test.db"))

    with patch.dict("os.environ", {"PYAPID_DB": tmp_file}):
        assert db.insert("avgo", "2020-01-01", "2020-01-02", [{"a": 1}]) == [
            {
                "uuid": "1234",
                "stock": "avgo",
                "start": "2020-01-01",
                "end": "2020-01-02",
                "data": json.dumps([{"a": 1}]),
            }
        ]
