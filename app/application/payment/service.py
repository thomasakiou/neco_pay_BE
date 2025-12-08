from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.payment import Payment
from app.infrastructure.repository import PaymentRepository
from app.infrastructure.models import PostingModel, StaffModel, ParameterModel, DistanceModel

class PaymentService:
    def __init__(self, repository: PaymentRepository, db: Session):
        self.repository = repository
        self.db = db

    def generate_payments(self, payment_title: str, numb_of_nights: int, local_runs: float) -> int:
        postings = self.db.query(PostingModel).all()
        parameters = self.db.query(ParameterModel).all()
        distances = self.db.query(DistanceModel).all()
        staff_list = self.db.query(StaffModel).all()
        
        # Create lookup maps for performance
        staff_map = {s.staff_id: s for s in staff_list if s.staff_id}
        
        # Parameter lookup: Key = last 2 digits of contiss
        param_map = {}
        for p in parameters:
            if p.contiss:
                key = p.contiss.strip()[-2:] # Last 2 digits
                param_map[key] = p

        # Distance lookup: Key = (source, target)
        dist_map = {}
        for d in distances:
            if d.source and d.target:
                dist_map[(d.source.strip().lower(), d.target.strip().lower())] = d
        
        new_payments = []
        
        for posting in postings:
            # 1. Link Staff & Posting (Staff.staff_id == Posting.file_no)
            staff = staff_map.get(posting.file_no)
            
            # Logic: Need both posting and staff link? 
            # Request says: Per_No(from staff table). If no staff link, we might not have Per_No or Bank info.
            # Assuming we generate only if link exists or at least partially?
            # Let's try to populate what we can.
            
            per_no = staff.staff_id if staff else None
            bank_account = staff.account_no if staff else None
            
            # 2. Get Amount Per Night (Parameter.pernight where last 2 digits contiss = conraiss in posting)
            amount_per_night = 0.0
            km_rate = 0.0
            
            if posting.conraiss:
                conraiss_suffix = posting.conraiss.strip()[-2:]
                param = param_map.get(conraiss_suffix)
                if param:
                    amount_per_night = param.pernight or 0.0
                    km_rate = param.kilometer or 0.0

            # 3. Get Transport (Parameter.kilometer * Distance.distance)
            transport = 0.0
            distance_val = 0.0
            
            if posting.station and posting.posting:
                source = posting.station.strip().lower()
                target = posting.posting.strip().lower()
                
                dist_obj = dist_map.get((source, target))
                if dist_obj:
                     distance_val = dist_obj.distance or 0.0
                else: 
                     # Try reversed? Or just 0. Usually distance is directional or symmetric defined in DB.
                     pass
            
            transport = km_rate * distance_val
            
            # 4. NetPay
            # netpay = transport + local_runs + (numb_of_nights * amount_per_night)
            netpay = transport + local_runs + (numb_of_nights * amount_per_night)

            payment = Payment(
                id=None,
                per_no=per_no,
                name=posting.name, # name (from posting table)
                station=posting.station,
                posting=posting.posting,
                bank_account=bank_account,
                transport=transport,
                local_runs=local_runs,
                numb_of_nights=numb_of_nights,
                amount_per_night=amount_per_night,
                netpay=netpay,
                payment_title=payment_title,
                created_at=None
            )
            new_payments.append(payment)

        self.repository.bulk_save(new_payments)
        return len(new_payments)

    def delete_all(self):
        self.repository.delete_all()
