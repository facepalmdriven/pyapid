"""
Main file, routes are here, this is what the app server will load and run.

TODO: Can we do this without the global?
"""

from fastapi import FastAPI, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from pyapid.types import Data, PyapidParseError
import pyapid.reports as reports


app = FastAPI()


@app.get("/")
@app.get("/reports")
def get_all_reports():
    result = reports.get()

    if result:
        return result
    else:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No reports found.")


@app.get("/reports/{report_id}")
def get_report(report_id: str):
    result = reports.get(report_id)

    if result:
        return result
    else:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Report not found")


@app.post("/reports/create", status_code=HTTP_201_CREATED)
def update_report(data: Data):
    try:
        return reports.create(data)
    except PyapidParseError:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Bad query")
