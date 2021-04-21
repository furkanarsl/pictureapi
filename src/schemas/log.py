from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from datetime import datetime


class LogSchema(BaseModel):
    picture_path: str
    query_date: datetime
    result: str


class LogSchemaListTest(BaseModel):
    history: list[LogSchema]


from src.models import Log

LogSchemaList = pydantic_queryset_creator(Log)
