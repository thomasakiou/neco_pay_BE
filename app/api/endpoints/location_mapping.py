from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.application.auth.dependencies import get_current_user
from app.application.location_mapping.dtos import LocationMappingDTO, SaveLocationMappingDTO
from app.domain.user import User
from app.infrastructure.database import SessionLocal
from app.infrastructure.models import DistanceModel, LocationMappingModel

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[LocationMappingDTO])
def list_location_mappings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(LocationMappingModel).order_by(
        LocationMappingModel.field_type,
        LocationMappingModel.original_value,
    ).all()


@router.put("/", response_model=LocationMappingDTO)
def save_location_mapping(
    dto: SaveLocationMappingDTO,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    original_value = dto.original_value.strip()
    canonical_value = dto.canonical_value.strip()
    if not original_value or not canonical_value:
        raise HTTPException(status_code=422, detail="Original and mapped locations are required.")

    is_source = dto.field_type == "station"
    location_column = DistanceModel.source if is_source else DistanceModel.target
    canonical_locations = [
        value for (value,) in db.query(location_column).filter(location_column.isnot(None)).distinct()
        if value and value.strip().casefold() == canonical_value.casefold()
    ]
    if not canonical_locations:
        side = "Source" if is_source else "Target"
        raise HTTPException(status_code=422, detail=f"Mapped value must match a Distance {side} value.")
    canonical_value = canonical_locations[0].strip()

    mappings = db.query(LocationMappingModel).filter(
        LocationMappingModel.field_type == dto.field_type
    ).all()
    existing = next(
        (mapping for mapping in mappings if mapping.original_value.strip().casefold() == original_value.casefold()),
        None,
    )
    if existing:
        existing.original_value = original_value
        existing.canonical_value = canonical_value
        db_mapping = existing
    else:
        db_mapping = LocationMappingModel(
            field_type=dto.field_type,
            original_value=original_value,
            canonical_value=canonical_value,
        )
        db.add(db_mapping)

    db.commit()
    db.refresh(db_mapping)
    return db_mapping


@router.delete("/{mapping_id}", status_code=204)
def delete_location_mapping(
    mapping_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    mapping = db.query(LocationMappingModel).filter(LocationMappingModel.id == mapping_id).first()
    if not mapping:
        raise HTTPException(status_code=404, detail="Location mapping not found.")
    db.delete(mapping)
    db.commit()
