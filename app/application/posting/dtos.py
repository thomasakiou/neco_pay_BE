from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PostingBase(BaseModel):
    state: Optional[str] = None
    file_no: Optional[str] = None
    name: Optional[str] = None
    conraiss: Optional[str] = None
    station: Optional[str] = None
    posting: Optional[str] = None # Maps to 'Posted To'
    
    # state: Optional[str] = None
    # category: Optional[str] = None
    # rank: Optional[str] = None
    # mandate: Optional[str] = None
    active: bool = True

class CreatePostingDTO(PostingBase):
    pass

class UpdatePostingDTO(PostingBase):
    pass

class PostingDTO(PostingBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
