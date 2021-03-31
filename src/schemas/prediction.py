from pydantic import BaseModel


class PredictionParameters(BaseModel):
    hash: str
    p1: str


class Result(BaseModel):
    name: str
    ranking: float


class PredictionResult(BaseModel):
    results: list[Result]
