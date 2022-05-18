from fastapi.testclient import TestClient

from pyapid.api import app

client = TestClient(app)


def test_read_root():
    """TODO: /root must be ok"""

    r = client.get("/")

    assert r.status_code == 200
    assert r.json() == {"Hello": "World"}


def test_reports():
    """TODO: /reports must output a list of reports with their status"""


def test_submit():
    """
    /report/submit must let us submit a new report for processing
    accepted formats are JSON and CSV, anything else should result in an error
    """


def test_access_in_progress():
    """TODO: Accessing specific report before it is ready should result in an error"""
