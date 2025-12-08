from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Posting:
    id: Optional[int]
    state: Optional[str] = None
    file_no: Optional[str] = None
    name: Optional[str] = None
    conraiss: Optional[str] = None
    station: Optional[str] = None
    posting: Optional[str] = None
    # Optional fields that might be null in new schema
    # state: Optional[str] = None
    # category: Optional[str] = None
    # rank: Optional[str] = None
    # mandate: Optional[str] = None
    active: bool = True
    created_at: Optional[datetime] = None
