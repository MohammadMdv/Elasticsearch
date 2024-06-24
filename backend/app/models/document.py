from pydantic import BaseModel
from typing import Optional, Dict, Any


class Document(BaseModel):
    index_name: str
    body: Dict[str, Any]
    doc_id: Optional[str] = None
