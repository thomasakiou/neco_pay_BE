from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from app.infrastructure.database import SessionLocal
from app.infrastructure.repository import PaymentRepository, StaffRepository
from app.application.payment.dtos import PaymentDTO, CreatePaymentDTO, UpdatePaymentDTO
from app.application.payment.service import PaymentService
from app.domain.payment import Payment

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_repository(db: Session = Depends(get_db)):
    return PaymentRepository(db)

def get_staff_repository(db: Session = Depends(get_db)):
    return StaffRepository(db)

def get_service(repo: PaymentRepository = Depends(get_repository), db: Session = Depends(get_db), staff_repo: StaffRepository = Depends(get_staff_repository)):
    return PaymentService(repo, db, staff_repo)

@router.get("/", response_model=List[PaymentDTO])
def list_payments(skip: int = 0, limit: int = 100000, repo: PaymentRepository = Depends(get_repository)):
    return repo.list(skip, limit)

@router.post("/", response_model=PaymentDTO)
def create_payment(dto: CreatePaymentDTO, repo: PaymentRepository = Depends(get_repository)):
    payment = Payment(
        id=None,
        created_at=None,
        **dto.dict(exclude_unset=True)
    )
    return repo.save(payment)

@router.get("/{id}", response_model=PaymentDTO)
def get_payment(id: int, repo: PaymentRepository = Depends(get_repository)):
    payment = repo.get_by_id(id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@router.put("/{id}", response_model=PaymentDTO)
def update_payment(id: int, dto: UpdatePaymentDTO, repo: PaymentRepository = Depends(get_repository)):
    payment = Payment(
        id=id,
        created_at=None,
        **dto.dict(exclude_unset=True)
    )
    updated_payment = repo.update(id, payment)
    if not updated_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return updated_payment

@router.delete("/", status_code=204)
def delete_all_payments(service: PaymentService = Depends(get_service)):
    service.delete_all()
    return

@router.delete("/{id}", status_code=204)
def delete_payment(id: int, repo: PaymentRepository = Depends(get_repository)):
    success = repo.delete(id)
    if not success:
        raise HTTPException(status_code=404, detail="Payment not found")
    return

from fastapi import File, UploadFile

@router.post("/upload", status_code=201)
async def upload_payments(file: UploadFile = File(...), service: PaymentService = Depends(get_service)):
    content = await file.read()
    # Decode string
    content_str = content.decode('utf-8')
    count = service.upload_payments(content_str)
    return {"message": f"Successfully uploaded {count} payments"}
