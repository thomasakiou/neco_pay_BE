from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import List
from sqlalchemy.orm import Session

from app.infrastructure.database import SessionLocal
from app.infrastructure.repository import StaffRepository
from app.application.staff.dtos import StaffDTO, CreateStaffDTO, UpdateStaffDTO
from app.application.staff.service import StaffService
from app.domain.staff import Staff
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
    return StaffRepository(db)

def get_service(repo: StaffRepository = Depends(get_repository)):
    return StaffService(repo)

@router.get("/", response_model=List[StaffDTO])
def list_staff(skip: int = 0, limit: int = 100000, repo: StaffRepository = Depends(get_repository), current_user: User = Depends(get_current_user)):
    return repo.list(skip, limit)

@router.post("/", response_model=StaffDTO)
def create_staff(dto: CreateStaffDTO, repo: StaffRepository = Depends(get_repository), current_user: User = Depends(get_current_user)):
    staff = Staff(
        id=None,
        created_at=None,
        **dto.dict(exclude_unset=True)
    )
    return repo.save(staff)

@router.get("/{id}", response_model=StaffDTO)
def get_staff(id: int, repo: StaffRepository = Depends(get_repository), current_user: User = Depends(get_current_user)):
    staff = repo.get_by_id(id)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")
    return staff

@router.put("/{id}", response_model=StaffDTO)
def update_staff(id: int, dto: UpdateStaffDTO, repo: StaffRepository = Depends(get_repository), current_user: User = Depends(get_current_user)):
    staff = Staff(
        id=id,
        created_at=None,
        **dto.dict(exclude_unset=True) 
    )
    
    updated_staff = repo.update(id, staff)
    if not updated_staff:
        raise HTTPException(status_code=404, detail="Staff not found")
    return updated_staff

@router.delete("/", status_code=204)
def delete_all_staff(repo: StaffRepository = Depends(get_repository), current_user: User = Depends(get_current_user)):
    repo.delete_all()
    return

@router.delete("/{id}", status_code=204)
def delete_staff(id: int, repo: StaffRepository = Depends(get_repository), current_user: User = Depends(get_current_user)):
    success = repo.delete(id)
    if not success:
        raise HTTPException(status_code=404, detail="Staff not found")
    return

@router.post("/reset-posted")
def reset_posted(repo: StaffRepository = Depends(get_repository), current_user: User = Depends(get_current_user)):
    repo.reset_posted_status()
    return {"message": "Successfully reset posted status for all staff"}

@router.post("/upload")
async def upload_staff(file: UploadFile = File(...), service: StaffService = Depends(get_service), current_user: User = Depends(get_current_user)):
    count = await service.process_upload(file)
    return {"message": f"Successfully processed {count} records"}
