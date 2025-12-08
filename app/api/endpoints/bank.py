from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import List
from sqlalchemy.orm import Session

from app.infrastructure.database import SessionLocal
from app.infrastructure.repository import BankRepository
from app.application.bank.dtos import BankDTO, CreateBankDTO, UpdateBankDTO
from app.application.bank.service import BankService
from app.domain.bank import Bank

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_repository(db: Session = Depends(get_db)):
    return BankRepository(db)

def get_service(repo: BankRepository = Depends(get_repository)):
    return BankService(repo)

@router.get("/", response_model=List[BankDTO])
def list_banks(skip: int = 0, limit: int = 100000, repo: BankRepository = Depends(get_repository)):
    return repo.list(skip, limit)

@router.post("/", response_model=BankDTO)
def create_bank(dto: CreateBankDTO, repo: BankRepository = Depends(get_repository)):
    bank = Bank(
        id=None,
        created_at=None,
        **dto.dict(exclude_unset=True)
    )
    return repo.save(bank)

@router.get("/{id}", response_model=BankDTO)
def get_bank(id: int, repo: BankRepository = Depends(get_repository)):
    bank = repo.get_by_id(id)
    if not bank:
        raise HTTPException(status_code=404, detail="Bank not found")
    return bank

@router.put("/{id}", response_model=BankDTO)
def update_bank(id: int, dto: UpdateBankDTO, repo: BankRepository = Depends(get_repository)):
    bank = Bank(
        id=id,
        created_at=None,
        **dto.dict(exclude_unset=True)
    )
    updated_bank = repo.update(id, bank)
    if not updated_bank:
        raise HTTPException(status_code=404, detail="Bank not found")
    return updated_bank

@router.delete("/", status_code=204)
def delete_all_banks(repo: BankRepository = Depends(get_repository)):
    repo.delete_all()
    return

@router.delete("/{id}", status_code=204)
def delete_bank(id: int, repo: BankRepository = Depends(get_repository)):
    success = repo.delete(id)
    if not success:
        raise HTTPException(status_code=404, detail="Bank not found")
    return

@router.post("/upload")
async def upload_banks(file: UploadFile = File(...), service: BankService = Depends(get_service)):
    count = await service.process_upload(file)
    return {"message": f"Successfully processed {count} records"}
