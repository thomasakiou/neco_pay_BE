from sqlalchemy.orm import Session
from typing import List, Optional
from app.domain.payment import Payment
from app.application.interfaces import IPaymentRepository
from app.infrastructure.models import PaymentModel

class PaymentRepository(IPaymentRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, payment: Payment) -> Payment:
        db_payment = PaymentModel.from_entity(payment)
        self.db.add(db_payment)
        self.db.commit()
        self.db.refresh(db_payment)
        return db_payment.to_entity()

    def get_by_id(self, id: int) -> Optional[Payment]:
        db_payment = self.db.query(PaymentModel).filter(PaymentModel.id == id).first()
        return db_payment.to_entity() if db_payment else None

    def list(self, skip: int = 0, limit: int = 100) -> List[Payment]:
        db_payments = self.db.query(PaymentModel).offset(skip).limit(limit).all()
        return [p.to_entity() for p in db_payments]

    def delete(self, id: int) -> bool:
        db_payment = self.db.query(PaymentModel).filter(PaymentModel.id == id).first()
        if db_payment:
            self.db.delete(db_payment)
            self.db.commit()
            return True
        return False
    
    def delete_all(self):
         self.db.query(PaymentModel).delete()
         self.db.commit()

    def bulk_save(self, payments: List[Payment]):
        for payment in payments:
            self.save(payment)
            
    def update(self, id: int, payment: Payment) -> Optional[Payment]:
        existing = self.db.query(PaymentModel).filter(PaymentModel.id == id).first()
        if not existing:
            return None
            
        for key, value in payment.__dict__.items():
            if key != 'id' and key != 'created_at':
                setattr(existing, key, value)
        
        self.db.commit()
        self.db.refresh(existing)
        return existing.to_entity()

from app.domain.staff import Staff
from app.infrastructure.models import StaffModel

class StaffRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, staff: Staff) -> Staff:
        # Check if exists by staff_id to update or create? 
        # For now, simple create. Ideally upsert.
        db_staff = StaffModel.from_entity(staff)
        
        # Check if exists (Upsert logic)
        existing = self.db.query(StaffModel).filter(StaffModel.staff_id == staff.staff_id).first()
        if existing:
            # Update fields
            for key, value in staff.__dict__.items():
                if key != 'id' and key != 'created_at':
                    setattr(existing, key if key != 'union' and key != 'group_code' else ('union_val' if key == 'union' else 'group_code'), value)
            self.db.commit()
            self.db.refresh(existing)
            return existing.to_entity()
        
        self.db.add(db_staff)
        self.db.commit()
        self.db.refresh(db_staff)
        return db_staff.to_entity()

    def get_by_id(self, id: int) -> Optional[Staff]:
        db_staff = self.db.query(StaffModel).filter(StaffModel.id == id).first()
        return db_staff.to_entity() if db_staff else None
    
    def get_by_staff_id(self, staff_id: str) -> Optional[Staff]:
        db_staff = self.db.query(StaffModel).filter(StaffModel.staff_id == staff_id).first()
        return db_staff.to_entity() if db_staff else None

    def list(self, skip: int = 0, limit: int = 100) -> List[Staff]:
        db_staffs = self.db.query(StaffModel).offset(skip).limit(limit).all()
        return [s.to_entity() for s in db_staffs]

    def delete(self, id: int) -> bool:
        db_staff = self.db.query(StaffModel).filter(StaffModel.id == id).first()
        if db_staff:
            self.db.delete(db_staff)
            self.db.commit()
            return True
        return False

    def delete_all(self):
        self.db.query(StaffModel).delete()
        self.db.commit()

    def bulk_save(self, staffs: List[Staff]):
        # This can be optimized with bulk_insert_mappings but iterating is safer for now due to potential duplicates
        # Or use bulk_save_objects
        # Using a simple loop for now, optimize if slow
        for staff in staffs:
            self.save(staff) # Reusing save for upsert logic

    def reset_posted_status(self):
        self.db.query(StaffModel).update({StaffModel.posted: "N"})
        self.db.commit()

    def update_posted_status_by_file_no(self, file_no: str, posted_status: str = "Y") -> bool:
        """Update the posted status for a staff member by their file_no (staff_id)"""
        staff = self.db.query(StaffModel).filter(StaffModel.staff_id == file_no).first()
        if staff:
            staff.posted = posted_status
            self.db.commit()
            return True
        return False

    def update(self, id: int, staff: Staff) -> Optional[Staff]:
        existing = self.db.query(StaffModel).filter(StaffModel.id == id).first()
        if not existing:
             return None
        
        # Update fields
        for key, value in staff.__dict__.items():
            if key != 'id' and key != 'created_at':
                 setattr(existing, key if key != 'union' and key != 'group_code' else ('union_val' if key == 'union' else 'group_code'), value)
        
        self.db.commit()
        self.db.refresh(existing)
        return existing.to_entity()

from app.domain.bank import Bank
from app.infrastructure.models import BankModel

class BankRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, bank: Bank) -> Bank:
        db_bank = BankModel.from_entity(bank)
        self.db.add(db_bank)
        self.db.commit()
        self.db.refresh(db_bank)
        return db_bank.to_entity()

    def get_by_id(self, id: int) -> Optional[Bank]:
        db_bank = self.db.query(BankModel).filter(BankModel.id == id).first()
        return db_bank.to_entity() if db_bank else None

    def list(self, skip: int = 0, limit: int = 100) -> List[Bank]:
        db_banks = self.db.query(BankModel).offset(skip).limit(limit).all()
        return [b.to_entity() for b in db_banks]

    def delete(self, id: int) -> bool:
        db_bank = self.db.query(BankModel).filter(BankModel.id == id).first()
        if db_bank:
            self.db.delete(db_bank)
            self.db.commit()
            return True
        return False

    def delete_all(self):
        self.db.query(BankModel).delete()
        self.db.commit()

    def bulk_save(self, banks: List[Bank]):
        # Simple iteration for now
        for bank in banks:
            self.save(bank)

    def update(self, id: int, bank: Bank) -> Optional[Bank]:
        existing = self.db.query(BankModel).filter(BankModel.id == id).first()
        if not existing:
            return None
        
        for key, value in bank.__dict__.items():
            if key != 'id' and key != 'created_at':
                setattr(existing, key, value)
        
        self.db.commit()
        self.db.refresh(existing)
        return existing.to_entity()

from app.domain.distance import Distance
from app.infrastructure.models import DistanceModel

class DistanceRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, distance: Distance) -> Distance:
        db_distance = DistanceModel.from_entity(distance)
        self.db.add(db_distance)
        self.db.commit()
        self.db.refresh(db_distance)
        return db_distance.to_entity()

    def get_by_id(self, id: int) -> Optional[Distance]:
        db_distance = self.db.query(DistanceModel).filter(DistanceModel.id == id).first()
        return db_distance.to_entity() if db_distance else None

    def list(self, skip: int = 0, limit: int = 100) -> List[Distance]:
        db_distances = self.db.query(DistanceModel).offset(skip).limit(limit).all()
        return [d.to_entity() for d in db_distances]

    def delete(self, id: int) -> bool:
        db_distance = self.db.query(DistanceModel).filter(DistanceModel.id == id).first()
        if db_distance:
            self.db.delete(db_distance)
            self.db.commit()
            return True
        return False

    def delete_all(self):
        self.db.query(DistanceModel).delete()
        self.db.commit()

    def bulk_save(self, distances: List[Distance]):
        # Simple iteration
        for distance in distances:
            self.save(distance)

    def update(self, id: int, distance: Distance) -> Optional[Distance]:
        existing = self.db.query(DistanceModel).filter(DistanceModel.id == id).first()
        if not existing:
            return None
        
        for key, value in distance.__dict__.items():
            if key != 'id' and key != 'created_at':
                setattr(existing, key, value)
        
        self.db.commit()
        self.db.refresh(existing)
        return existing.to_entity()

from app.domain.parameter import Parameter
from app.infrastructure.models import ParameterModel

class ParameterRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, parameter: Parameter) -> Parameter:
        db_parameter = ParameterModel.from_entity(parameter)
        self.db.add(db_parameter)
        self.db.commit()
        self.db.refresh(db_parameter)
        return db_parameter.to_entity()

    def get_by_id(self, id: int) -> Optional[Parameter]:
        db_parameter = self.db.query(ParameterModel).filter(ParameterModel.id == id).first()
        return db_parameter.to_entity() if db_parameter else None

    def list(self, skip: int = 0, limit: int = 100) -> List[Parameter]:
        db_parameters = self.db.query(ParameterModel).offset(skip).limit(limit).all()
        return [p.to_entity() for p in db_parameters]

    def delete(self, id: int) -> bool:
        db_parameter = self.db.query(ParameterModel).filter(ParameterModel.id == id).first()
        if db_parameter:
            self.db.delete(db_parameter)
            self.db.commit()
            return True
        return False

    def delete_all(self):
        self.db.query(ParameterModel).delete()
        self.db.commit()

    def bulk_save(self, parameters: List[Parameter]):
        for parameter in parameters:
            self.save(parameter)

    def update(self, id: int, parameter: Parameter) -> Optional[Parameter]:
        existing = self.db.query(ParameterModel).filter(ParameterModel.id == id).first()
        if not existing:
            return None
        
        for key, value in parameter.__dict__.items():
            if key != 'id' and key != 'created_at':
                setattr(existing, key, value)
        
        self.db.commit()
        self.db.refresh(existing)
        return existing.to_entity()

from app.domain.posting import Posting
from app.infrastructure.models import PostingModel

class PostingRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, posting: Posting) -> Posting:
        db_posting = PostingModel.from_entity(posting)
        self.db.add(db_posting)
        self.db.commit()
        self.db.refresh(db_posting)
        return db_posting.to_entity()

    def get_by_id(self, id: int) -> Optional[Posting]:
        db_posting = self.db.query(PostingModel).filter(PostingModel.id == id).first()
        return db_posting.to_entity() if db_posting else None

    def list(self, skip: int = 0, limit: int = 100) -> List[Posting]:
        db_postings = self.db.query(PostingModel).offset(skip).limit(limit).all()
        return [p.to_entity() for p in db_postings]

    def delete(self, id: int) -> bool:
        db_posting = self.db.query(PostingModel).filter(PostingModel.id == id).first()
        if db_posting:
            self.db.delete(db_posting)
            self.db.commit()
            return True
        return False

    def delete_all(self):
        self.db.query(PostingModel).delete()
        self.db.commit()

    def bulk_save(self, postings: List[Posting]):
        for posting in postings:
            self.save(posting)

    def update(self, id: int, posting: Posting) -> Optional[Posting]:
        existing = self.db.query(PostingModel).filter(PostingModel.id == id).first()
        if not existing:
            return None
        
        for key, value in posting.__dict__.items():
            if key != 'id' and key != 'created_at':
                setattr(existing, key, value)
        
        self.db.commit()
        self.db.refresh(existing)
        return existing.to_entity()

from app.domain.state import State
from app.infrastructure.models import StateModel

class StateRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, state: State) -> State:
        db_state = StateModel.from_entity(state)
        self.db.add(db_state)
        self.db.commit()
        self.db.refresh(db_state)
        return db_state.to_entity()

    def get_by_id(self, id: int) -> Optional[State]:
        db_state = self.db.query(StateModel).filter(StateModel.id == id).first()
        return db_state.to_entity() if db_state else None

    def list(self, skip: int = 0, limit: int = 100) -> List[State]:
        db_states = self.db.query(StateModel).offset(skip).limit(limit).all()
        return [s.to_entity() for s in db_states]

    def delete(self, id: int) -> bool:
        db_state = self.db.query(StateModel).filter(StateModel.id == id).first()
        if db_state:
            self.db.delete(db_state)
            self.db.commit()
            return True
        return False

    def delete_all(self):
        self.db.query(StateModel).delete()
        self.db.commit()

    def bulk_save(self, states: List[State]):
        for state in states:
            self.save(state)

    def update(self, id: int, state: State) -> Optional[State]:
        existing = self.db.query(StateModel).filter(StateModel.id == id).first()
        if not existing:
            return None
        
        for key, value in state.__dict__.items():
            if key != 'id' and key != 'created_at':
                setattr(existing, key, value)
        
        self.db.commit()
        self.db.refresh(existing)
        return existing.to_entity()
