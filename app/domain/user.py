from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    id: Optional[int]
    username: str
    hashed_password: str
    role: str = "admin"  # admin, user, etc.
    active: bool = True
    created_at: Optional[datetime] = None
