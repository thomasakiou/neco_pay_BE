from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import List
from sqlalchemy.orm import Session

from app.infrastructure.database import SessionLocal
from app.infrastructure.repository import PostingRepository
from app.application.posting.dtos import PostingDTO, CreatePostingDTO, UpdatePostingDTO
from app.application.posting.service import PostingService
from app.domain.posting import Posting
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
    return PostingRepository(db)

def get_service(repo: PostingRepository = Depends(get_repository)):
    return PostingService(repo)

@router.get("/", response_model=List[PostingDTO])
def list_postings(skip: int = 0, limit: int = 100000, repo: PostingRepository = Depends(get_repository), current_user: User = Depends(get_current_user)):
    return repo.list(skip, limit)

@router.post("/", response_model=PostingDTO)
def create_posting(dto: CreatePostingDTO, repo: PostingRepository = Depends(get_repository), current_user: User = Depends(get_current_user)):
    posting = Posting(
        id=None,
        created_at=None,
        **dto.dict(exclude_unset=True)
    )
    return repo.save(posting)

@router.get("/{id}", response_model=PostingDTO)
def get_posting(id: int, repo: PostingRepository = Depends(get_repository), current_user: User = Depends(get_current_user)):
    posting = repo.get_by_id(id)
    if not posting:
        raise HTTPException(status_code=404, detail="Posting not found")
    return posting

@router.put("/{id}", response_model=PostingDTO)
def update_posting(id: int, dto: UpdatePostingDTO, repo: PostingRepository = Depends(get_repository), current_user: User = Depends(get_current_user)):
    posting = Posting(
        id=id,
        created_at=None,
        **dto.dict(exclude_unset=True)
    )
    updated_posting = repo.update(id, posting)
    if not updated_posting:
        raise HTTPException(status_code=404, detail="Posting not found")
    return updated_posting

@router.delete("/", status_code=204)
def delete_all_postings(repo: PostingRepository = Depends(get_repository), current_user: User = Depends(get_current_user)):
    repo.delete_all()
    return

@router.delete("/{id}", status_code=204)
def delete_posting(id: int, repo: PostingRepository = Depends(get_repository), current_user: User = Depends(get_current_user)):
    success = repo.delete(id)
    if not success:
        raise HTTPException(status_code=404, detail="Posting not found")
    return

@router.post("/upload")
async def upload_postings(file: UploadFile = File(...), service: PostingService = Depends(get_service), current_user: User = Depends(get_current_user)):
    count = await service.process_upload(file)
    return {"message": f"Successfully processed {count} records"}

@router.post("/generate", status_code=201)
def generate_payments_from_postings(payment_title: str, numb_of_nights: int, local_runs: float, service: PostingService = Depends(get_service), current_user: User = Depends(get_current_user)):
    """
    Generate payments based on all postings.
    Same logic as /payments/generate
    """
    count = service.generate_payments(
        payment_title=payment_title,
        numb_of_nights=numb_of_nights,
        local_runs=local_runs
    )
    return {"message": f"Successfully generated {count} payments from postings"}
