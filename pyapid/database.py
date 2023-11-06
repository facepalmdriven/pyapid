"""
Database connectivity
"""

import json
import sqlite3 as sql
from datetime import datetime
from uuid import uuid4

from pyapid.config import config


def init():
    """
    Create the database and tables if they do not exist.

    Returns the connection.
    """

    query = """
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY,
        uuid TEXT,
        stock TEXT,
        start INTEGER,
        end INTEGER,
        data TEXT,
        modified_at INTEGER
    )"""

    con = sql.connect(config().db)
    con.execute(query)
    con.commit()

    return con


def select(uuid=None) -> list[dict]:
    """
    Run a specified SQL query against the database.
    """

    query = "SELECT uuid, stock, start, end, data FROM reports"
    cursor = init().cursor()

    if uuid is not None:
        query += " WHERE uuid = ?"
        cursor = cursor.execute(query, (uuid,))
    else:
        cursor = cursor.execute(query)

    columns = [r[0] for r in cursor.description]
    data = []

    while record := cursor.fetchone():
        data.append(dict(zip(columns, record)))

    return data


def insert(stock, start, end, data, uuid=None):
    """
    Insert a new report into the database.
    """

    query = """
    INSERT INTO reports (uuid, stock, start, end, data, modified_at)
    VALUES (?, ?, ?, ?, ?, ?)"""

    uuid = uuid or str(uuid4())
    modified_at = int(datetime.now().timestamp())
    con = init()

    con.cursor().execute(
        query, (uuid, stock, start, end, json.dumps(data), modified_at)
    )
    con.commit()

    return select(uuid)
