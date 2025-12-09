from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import List
from sqlalchemy.orm import Session

from app.infrastructure.database import SessionLocal
from app.infrastructure.repository import ParameterRepository
from app.application.parameter.dtos import ParameterDTO, CreateParameterDTO, UpdateParameterDTO
from app.application.parameter.service import ParameterService
from app.domain.parameter import Parameter
from app.application.auth.dependencies import get_current_user
from app.domain.user import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_repository(db: Session = Depends(get_db)):
    return ParameterRepository(db)

def get_service(repo: ParameterRepository = Depends(get_repository)):
    return ParameterService(repo)

@router.get("/", response_model=List[ParameterDTO])
def list_parameters(skip: int = 0, limit: int = 100000, repo: ParameterRepository = Depends(get_repository), current_user: User = Depends(get_current_user)):
    return repo.list(skip, limit)

@router.post("/", response_model=ParameterDTO)
def create_parameter(dto: CreateParameterDTO, repo: ParameterRepository = Depends(get_repository), current_user: User = Depends(get_current_user)):
    parameter = Parameter(
        id=None,
        created_at=None,
        **dto.dict(exclude_unset=True)
    )
    return repo.save(parameter)

@router.get("/{id}", response_model=ParameterDTO)
def get_parameter(id: int, repo: ParameterRepository = Depends(get_repository), current_user: User = Depends(get_current_user)):
    parameter = repo.get_by_id(id)
    if not parameter:
        raise HTTPException(status_code=404, detail="Parameter not found")
    return parameter

@router.put("/{id}", response_model=ParameterDTO)
def update_parameter(id: int, dto: UpdateParameterDTO, repo: ParameterRepository = Depends(get_repository), current_user: User = Depends(get_current_user)):
    parameter = Parameter(
        id=id,
        created_at=None,
        **dto.dict(exclude_unset=True)
    )
    updated_parameter = repo.update(id, parameter)
    if not updated_parameter:
        raise HTTPException(status_code=404, detail="Parameter not found")
    return updated_parameter

@router.delete("/", status_code=204)
def delete_all_parameters(repo: ParameterRepository = Depends(get_repository), current_user: User = Depends(get_current_user)):
    repo.delete_all()
    return

@router.delete("/{id}", status_code=204)
def delete_parameter(id: int, repo: ParameterRepository = Depends(get_repository), current_user: User = Depends(get_current_user)):
    success = repo.delete(id)
    if not success:
        raise HTTPException(status_code=404, detail="Parameter not found")
    return

@router.post("/upload")
async def upload_parameters(file: UploadFile = File(...), service: ParameterService = Depends(get_service), current_user: User = Depends(get_current_user)):
    count = await service.process_upload(file)
    return {"message": f"Successfully processed {count} records"}
