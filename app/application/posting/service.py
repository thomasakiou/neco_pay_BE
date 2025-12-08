from typing import List
import pandas as pd
import tempfile
import os
from fastapi import UploadFile

from app.domain.posting import Posting
from app.infrastructure.repository import PostingRepository

class PostingService:
    def __init__(self, repository: PostingRepository):
        self.repository = repository

    async def process_upload(self, file: UploadFile) -> int:
        filename = file.filename
        content = await file.read()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        try:

            # 1. Read file to find header
            if filename.lower().endswith('.csv'):
                df_raw = pd.read_csv(tmp_path, header=None)
            elif filename.lower().endswith('.xlsx') or filename.lower().endswith('.xls'):
                df_raw = pd.read_excel(tmp_path, header=None)
            else:
                raise ValueError("Unsupported file format")

            # 2. Find header row index
            header_idx = -1
            for idx, row in df_raw.iterrows():
                row_str = str(row.values).upper()
                # New CSV target headers: FILE NO, NAME, CONRAISS, STATION, Posted To
                if ("FILE NO" in row_str or "FILE_NO" in row_str) and "NAME" in row_str and "STATION" in row_str:
                    header_idx = idx
                    break
            
            # 3. Read data with correct header
            if header_idx != -1:
                # Reload with header, skip rows before header
                if filename.lower().endswith('.csv'):
                    df = pd.read_csv(tmp_path, header=header_idx)
                else:
                    df = pd.read_excel(tmp_path, header=header_idx)
            else:
                # Fallback: assume first row is header if not found (or fail? let's try 0)
                if filename.lower().endswith('.csv'):
                   df = pd.read_csv(tmp_path)
                else:
                   df = pd.read_excel(tmp_path)

            # 4. (State Transformation Removed)
            
            data = df.to_dict('records')
            posting_list = []
            
            for row in data:
                # Clean row: replace NaN with None
                row = {k: (None if pd.isna(v) else v) for k, v in row.items()}
                
                # Normalize row keys for easier lookup
                row_normalized = {str(k).strip().upper(): v for k, v in row.items()}

                def get_val(target_key):
                    # Helper to find value by trying various key formats in PRIORITY order
                    candidates = [target_key, target_key.upper(), target_key.lower(), target_key.title()]
                    
                    # Specific aliases with priority
                    if target_key == 'file_no':
                        candidates = ['FILE NO', 'FILE No', 'File No', 'File_No', 'FILE_NO'] + candidates
                    if target_key == 'posting':
                        candidates = ['Posted To', 'posted to', 'POSTED TO'] + candidates
                    
                    for cand in candidates:
                        cand_upper = str(cand).strip().upper()
                        if cand_upper in row_normalized:
                             return row_normalized[cand_upper]
                    return None

                posting = Posting(
                    id=None,
                    # state=None, # Dropped
                    file_no=str(get_val('file_no') or ''),
                    name=str(get_val('name') or ''),
                    conraiss=str(get_val('conraiss') or ''),
                    station=str(get_val('station') or ''),
                    posting=str(get_val('posting') or ''), # Maps from 'Posted To'
                    
                    # Dropped fields
                    # category=None,
                    # rank=None,
                    # mandate=None,
                    
                    active=True,
                    created_at=None
                )
                
                # Basic check
                if posting.name or posting.file_no:
                     posting_list.append(posting)

            self.repository.bulk_save(posting_list)
            return len(posting_list)

        finally:
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except:
                    pass

    def generate_payments(self, payment_title: str, numb_of_nights: int, local_runs: float):
        """
        Generate payments based on posting data.
        This method has the same logic as PaymentService.generate_payments
        """
        from app.infrastructure.models import StaffModel, ParameterModel, DistanceModel, PaymentModel
        from app.domain.payment import Payment
        from sqlalchemy.orm import Session
        
        # Get DB session from repository
        db = self.repository.db
        
        postings = self.repository.list(skip=0, limit=100000)
        parameters = db.query(ParameterModel).all()
        distances = db.query(DistanceModel).all()
        staff_list = db.query(StaffModel).all()
        
        # Create lookup maps for performance
        staff_map = {s.staff_id: s for s in staff_list if s.staff_id}
        
        # Parameter lookup: Key = last 2 digits of contiss
        param_map = {}
        for p in parameters:
            if p.contiss:
                key = p.contiss.strip()[-2:]
                param_map[key] = p

        # Distance lookup: Key = (source, target)
        dist_map = {}
        for d in distances:
            if d.source and d.target:
                dist_map[(d.source.strip().lower(), d.target.strip().lower())] = d
        
        new_payments = []
        
        for posting in postings:
            # 1. Link Staff & Posting
            staff = staff_map.get(posting.file_no)
            
            per_no = staff.staff_id if staff else None
            bank_account = staff.account_no if staff else None
            
            # 2. Get Amount Per Night
            amount_per_night = 0.0
            km_rate = 0.0
            
            if posting.conraiss:
                conraiss_suffix = posting.conraiss.strip()[-2:]
                param = param_map.get(conraiss_suffix)
                if param:
                    amount_per_night = param.pernight or 0.0
                    km_rate = param.kilometer or 0.0

            # 3. Get Transport
            transport = 0.0
            distance_val = 0.0
            
            if posting.station and posting.posting:
                source = posting.station.strip().lower()
                target = posting.posting.strip().lower()
                
                dist_obj = dist_map.get((source, target))
                if dist_obj:
                     distance_val = dist_obj.distance or 0.0
            
            transport = km_rate * distance_val
            
            # 4. NetPay
            netpay = transport + local_runs + (numb_of_nights * amount_per_night)

            payment = Payment(
                id=None,
                per_no=per_no,
                name=posting.name,
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

        # Save payments using PaymentRepository
        from app.infrastructure.repository import PaymentRepository
        payment_repo = PaymentRepository(db)
        payment_repo.bulk_save(new_payments)
        
        return len(new_payments)
