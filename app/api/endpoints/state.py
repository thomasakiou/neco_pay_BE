from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List
# get_db is not in database.py, it's usually defined locally or we need SessionLocal
from app.infrastructure.database import SessionLocal
from app.infrastructure.repository import StateRepository
from app.application.state.service import StateService
from dataclasses import dataclass
from pydantic import BaseModel
from typing import Optional
from app.application.auth.dependencies import get_current_user
from app.domain.user import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models (can be moved to separate file later if needed to be strict cleanliness)
class StateCreate(BaseModel):
    code: str
    state: str
    capital: str

class StateResponse(BaseModel):
    id: int
    code: str
    state: str
    capital: str
    active: bool

    class Config:
        from_attributes = True

def get_service(db: Session = Depends(get_db)) -> StateService:
    repository = StateRepository(db)
    return StateService(repository)

@router.post("/", response_model=StateResponse)
def create_state(state: StateCreate, service: StateService = Depends(get_service), current_user: User = Depends(get_current_user)):
    from app.domain.state import State
    new_state = State(id=None, code=state.code, state=state.state, capital=state.capital)
    return service.create_state(new_state)

@router.get("/", response_model=List[StateResponse])
def list_states(skip: int = 0, limit: int = 100, service: StateService = Depends(get_service), current_user: User = Depends(get_current_user)):
    return service.get_states(skip, limit)

@router.put("/{id}", response_model=StateResponse)
def update_state(id: int, state: StateCreate, service: StateService = Depends(get_service)):
    from app.domain.state import State
    updated_state = State(id=id, code=state.code, state=state.state, capital=state.capital)
    result = service.update_state(id, updated_state)
    if not result:
        raise HTTPException(status_code=404, detail="State not found")
    return result

@router.delete("/delete-all")
def delete_all_states(service: StateService = Depends(get_service), current_user: User = Depends(get_current_user)):
    service.delete_all_states()
    return {"message": "All states deleted"}

@router.delete("/{id}")
def delete_state(id: int, service: StateService = Depends(get_service), current_user: User = Depends(get_current_user)):
    if service.delete_state(id):
        return {"message": "State deleted"}
    raise HTTPException(status_code=404, detail="State not found")

@router.post("/upload")
async def upload_states(file: UploadFile = File(...), service: StateService = Depends(get_service), current_user: User = Depends(get_current_user)):
    content = await file.read()
    count = service.upload_states(content, file.filename)
    return {"message": f"Successfully uploaded {count} states"}
