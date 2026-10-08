from typing import List
import pandas as pd
import tempfile
import os
from fastapi import UploadFile

from app.domain.posting import Posting
from app.infrastructure.repository import PostingRepository
from app.application.location_mapping.resolver import resolve_station_office_code

class PostingService:
    def __init__(self, repository: PostingRepository):
        self.repository = repository

    async def process_upload(self, file: UploadFile, batch_name: str) -> int:
        filename = file.filename
        content = await file.read()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        try:
            def read_csv(**kwargs):
                try:
                    return pd.read_csv(tmp_path, encoding='utf-8-sig', **kwargs)
                except UnicodeDecodeError:
                    return pd.read_csv(tmp_path, encoding='cp1252', **kwargs)

            # 1. Read file to find header
            if filename.lower().endswith('.csv'):
                df_raw = read_csv(header=None)
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
                    df = read_csv(header=header_idx)
                else:
                    df = pd.read_excel(tmp_path, header=header_idx)
            else:
                # Fallback: assume first row is header if not found (or fail? let's try 0)
                if filename.lower().endswith('.csv'):
                   df = read_csv()
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
                    if target_key == 'no_of_nights':
                        candidates = ['No_of_nights', 'NO_OF_NIGHTS', 'No of nights', 'Number of Nights'] + candidates
                    
                    for cand in candidates:
                        cand_upper = str(cand).strip().upper()
                        if cand_upper in row_normalized:
                             return row_normalized[cand_upper]
                    return None

                nights_value = get_val('no_of_nights')
                no_of_nights = None
                if nights_value is not None and str(nights_value).strip():
                    try:
                        nights_number = float(nights_value)
                    except (TypeError, ValueError) as error:
                        raise ValueError("No_of_nights values must be non-negative whole numbers.") from error
                    if not nights_number.is_integer() or nights_number < 0:
                        raise ValueError("No_of_nights values must be non-negative whole numbers.")
                    no_of_nights = int(nights_number)

                posting = Posting(
                    id=None,
                    file_no=str(get_val('file_no') or ''),
                    name=str(get_val('name') or ''),
                    conraiss=str(get_val('conraiss') or ''),
                    station=str(get_val('station') or ''),
                    posting=str(get_val('posting') or ''),
                    no_of_nights=no_of_nights,
                    batch_name=batch_name,
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
        from app.infrastructure.models import StaffModel, ParameterModel, DistanceModel, LocationMappingModel
        from app.domain.payment import Payment
        from sqlalchemy.orm import Session
        
        # Get DB session from repository
        db = self.repository.db
        
        postings = self.repository.list(skip=0, limit=100000)
        parameters = db.query(ParameterModel).all()
        distances = db.query(DistanceModel).all()
        staff_list = db.query(StaffModel).all()
        location_mappings = db.query(LocationMappingModel).all()
        
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

        location_map = {
            (mapping.field_type, mapping.original_value.strip().casefold()): mapping.canonical_value
            for mapping in location_mappings
        }
        
        new_payments = []
        
        for posting in postings:
            # 1. Link Staff & Posting
            staff = staff_map.get(posting.file_no)
            
            per_no = staff.staff_id if staff else None
            bank_account = staff.account_no if staff else None
            bank_name = staff.bank_name if staff else None
            
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
                source = (
                    resolve_station_office_code(
                        posting.station,
                        [distance.source for distance in distances],
                    )
                    or location_map.get(
                        ("station", posting.station.strip().casefold()),
                        posting.station.strip(),
                    )
                ).lower()
                target = location_map.get(
                    ("posted_to", posting.posting.strip().casefold()),
                    posting.posting.strip(),
                ).lower()
                
                dist_obj = dist_map.get((source, target))
                if dist_obj:
                     distance_val = dist_obj.distance or 0.0
            
            transport = km_rate * distance_val
            
            staff_nights = numb_of_nights + (posting.no_of_nights or 0)

            # 4. NetPay
            netpay = transport + local_runs + (staff_nights * amount_per_night)

            payment = Payment(
                id=None,
                file_no=per_no,
                name=posting.name,
                conraiss=posting.conraiss,
                bank=bank_name,
                account_numb=bank_account,
                station=posting.station,
                posting=posting.posting,
                transport=transport,
                fuel_local=local_runs,
                numb_of_nights=staff_nights,
                amount_per_night=amount_per_night,
                dta=staff_nights * amount_per_night,
                total=netpay,
                total_netpay=netpay,
                payment_title=payment_title,
                created_at=None
            )
            new_payments.append(payment)

        # Save payments using PaymentRepository
        from app.infrastructure.repository import PaymentRepository
        payment_repo = PaymentRepository(db)
        payment_repo.bulk_save(new_payments)
        
        return len(new_payments)
