from unittest.mock import patch

from fastapi.testclient import TestClient
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
)
import pytest

from pyapid.api import app


http = TestClient(app)


@pytest.fixture()
def temp_db(tmpdir):
    return str(tmpdir.join("test.db"))


def test_empty_db(temp_db):
    """/ should return list of reports."""
    with patch.dict("os.environ", {"PYAPID_DB": temp_db}):
        r = http.get("/")
        assert r.status_code == HTTP_404_NOT_FOUND
        assert r.json() == {"detail": "No reports found."}

        r = http.get("/reports/1234")
        assert r.status_code == HTTP_404_NOT_FOUND
        assert r.json() == {"detail": "Report not found"}


def test_inserting_a_record(temp_db):
    """
    /reports/{report_id} inserting a record should work

    TODO: Test the returned data as well, will need to mock reports.create
    """

    with patch.dict("os.environ", {"PYAPID_DB": temp_db}):
        # Working query
        r = http.post(
            "/reports/create",
            json={"stock": "avgo", "start": "2020-01-01", "end": "2020-01-02"},
        )
        assert r.status_code == HTTP_201_CREATED

        uuid = r.json()[0]["uuid"]
        r = http.get(f"/reports/{uuid}")
        assert r.status_code == HTTP_200_OK

        # Broken query
        r = http.post(
            "/reports/create",
            json={
                "stock": "DSNTEXISTWILLYNILLY",
                "start": "2017-01-01",
                "end": "2017-04-30",
            },
        )

        assert r.status_code == HTTP_400_BAD_REQUEST
        assert r.json() == {"detail": "Bad query"}
