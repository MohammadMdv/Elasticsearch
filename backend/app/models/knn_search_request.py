from pydantic import BaseModel
from typing import List


class KNNQuery(BaseModel):
    field: str
    query_vector: List[float]
    k: int = 2
    num_candidates: int = 500


class KNNRequest(BaseModel):
    index_name: str
    query: KNNQuery
