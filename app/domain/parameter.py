from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Parameter:
    id: Optional[int]
    contiss: Optional[str] = None
    pernight: Optional[float] = None
    local: Optional[float] = None
    kilometer: Optional[float] = None
    active: bool = True
    created_at: Optional[datetime] = None
