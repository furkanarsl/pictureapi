from pydantic import BaseModel
from typing import List


class PredictionParameters(BaseModel):
    hash: str
    p1: str


class Result(BaseModel):
    result: str


class PredictionResult(BaseModel):
    results: List[Result]
