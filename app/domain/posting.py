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
    no_of_nights: Optional[int] = None
    batch_name: Optional[str] = None
    active: bool = True
    created_at: Optional[datetime] = None
