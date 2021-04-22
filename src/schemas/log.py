from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_queryset_creator
from datetime import datetime
from typing import List

class LogSchema(BaseModel):
    picture_path: str
    query_date: datetime
    result: str


class LogSchemaListTest(BaseModel):
    history: List[LogSchema]


from src.models import Log

LogSchemaList = pydantic_queryset_creator(Log)
