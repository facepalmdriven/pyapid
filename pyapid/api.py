"""
Main file, routes are here, this is what the app server will load and run.

TODO: Can we do this without the global?
"""

from fastapi import FastAPI, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from pyapid.types import Data, PyapidParseError
from pyapid import reports
from pyapid.config import config

# Call config to make sure we are caching the values in the very begining
config()

app = FastAPI()


@app.get("/")
@app.get("/reports")
def get_all_reports() -> dict:
    if result := reports.get():
        return result
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No reports found.")


@app.get("/reports/{report_id}")
def get_report(report_id: str):
    if result := reports.get(report_id):
        return result
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Report not found")


@app.post("/reports/create", status_code=HTTP_201_CREATED)
def update_report(data: Data) -> list[dict]:
    try:
        return reports.create(data)
    except PyapidParseError as ex:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Bad query"
        ) from ex
