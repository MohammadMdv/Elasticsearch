from pydantic import BaseModel
from typing import List


class KNNQuery(BaseModel):
    field: str
    query_text: str
    k: int = 2
    num_candidates: int = 500


class KNNRequest(BaseModel):
    index_name: str
    query: KNNQuery
