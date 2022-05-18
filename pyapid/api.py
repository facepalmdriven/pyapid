from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

import pyapid.json as json
import pyapid.reports as reports


app = FastAPI()


# TODO: Do we even need this?
class Report(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


# TODO: Get all reports
@app.get("/")
@app.get("/reports")
def get_all_reports():
    pass


# TODO: Get a specific report
@app.get("/reports/{report_id}")
def get_report(report_id: int, q: Optional[str] = None):
    return json.dump(reports.get(report_id))


# TODO: Create a report
@app.post("/reports/create")
def update_report(report_id: int, data: Report):
    return {"item_name": item.name, "item_id": item_id}
