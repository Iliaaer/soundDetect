from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, MetaData, JSON

metadata = MetaData()

audiofile = Table(
    "audiofile",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String, nullable=True),
    Column("time", TIMESTAMP, default=datetime.utcnow),
    Column("device", String, nullable=True),
    Column("duration", String, nullable=True),
    Column("result", JSON, nullable=True),
)
