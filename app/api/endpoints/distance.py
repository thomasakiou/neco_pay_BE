from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import List
from sqlalchemy.orm import Session

from app.infrastructure.database import SessionLocal
from app.infrastructure.repository import DistanceRepository
from app.application.distance.dtos import DistanceDTO, CreateDistanceDTO, UpdateDistanceDTO
from app.application.distance.service import DistanceService
from app.domain.distance import Distance
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
    return DistanceRepository(db)

def get_service(repo: DistanceRepository = Depends(get_repository)):
    return DistanceService(repo)

@router.get("/", response_model=List[DistanceDTO])
def list_distances(skip: int = 0, limit: int = 100000, repo: DistanceRepository = Depends(get_repository), current_user: User = Depends(get_current_user)):
    return repo.list(skip, limit)

@router.post("/", response_model=DistanceDTO)
def create_distance(dto: CreateDistanceDTO, repo: DistanceRepository = Depends(get_repository), current_user: User = Depends(get_current_user)):
    distance = Distance(
        id=None,
        created_at=None,
        **dto.dict(exclude_unset=True)
    )
    return repo.save(distance)

@router.get("/{id}", response_model=DistanceDTO)
def get_distance(id: int, repo: DistanceRepository = Depends(get_repository), current_user: User = Depends(get_current_user)):
    distance = repo.get_by_id(id)
    if not distance:
        raise HTTPException(status_code=404, detail="Distance not found")
    return distance

@router.put("/{id}", response_model=DistanceDTO)
def update_distance(id: int, dto: UpdateDistanceDTO, repo: DistanceRepository = Depends(get_repository), current_user: User = Depends(get_current_user)):
    distance = Distance(
        id=id,
        created_at=None,
        **dto.dict(exclude_unset=True)
    )
    updated_distance = repo.update(id, distance)
    if not updated_distance:
        raise HTTPException(status_code=404, detail="Distance not found")
    return updated_distance

@router.delete("/", status_code=204)
def delete_all_distances(repo: DistanceRepository = Depends(get_repository), current_user: User = Depends(get_current_user)):
    repo.delete_all()
    return

@router.delete("/{id}", status_code=204)
def delete_distance(id: int, repo: DistanceRepository = Depends(get_repository), current_user: User = Depends(get_current_user)):
    success = repo.delete(id)
    if not success:
        raise HTTPException(status_code=404, detail="Distance not found")
    return

@router.post("/upload")
async def upload_distances(file: UploadFile = File(...), service: DistanceService = Depends(get_service), current_user: User = Depends(get_current_user)):
    count = await service.process_upload(file)
    return {"message": f"Successfully processed {count} records"}
