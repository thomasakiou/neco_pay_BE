from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.payment import Payment
from app.infrastructure.repository import PaymentRepository
from app.infrastructure.models import PostingModel, StaffModel, ParameterModel, DistanceModel

class PaymentService:
    def __init__(self, repository: PaymentRepository, db: Session, staff_repository=None):
        self.repository = repository
        self.db = db
        self.staff_repository = staff_repository

    def upload_payments(self, file_content: str) -> int:
        import csv
        from io import StringIO
        
        # Handle BOM if present
        if file_content.startswith('\ufeff'):
            file_content = file_content[1:]
            
        f = StringIO(file_content)
        reader = csv.DictReader(f)
        
        # Normalize fieldnames (strip whitespace)
        if reader.fieldnames:
            reader.fieldnames = [name.strip() for name in reader.fieldnames]
            
        # Helper to find key in row case-insensitively and with underscore/space swap
        def get_val(row, key):
            # Try exact match
            if key in row:
                return row[key]
                
            # Try variations
            key_lower = key.lower()
            key_norm = key_lower.replace('_', ' ')
            
            for k in row.keys():
                if not k: continue
                k_norm = k.strip().lower()
                if k_norm == key_lower:
                    return row[k]
                if k_norm == key_norm:
                    return row[k]
                if k_norm == key_lower.replace(' ', '_'):
                     return row[k]
                     
            return None

        # Helper for handling variations of specific known headers
        def get_field(row, keys):
            if isinstance(keys, str):
                keys = [keys]
            
            for k in keys:
                val = get_val(row, k)
                if val is not None:
                    return val
            return None

        def safe_float(val):
            if not val: return 0.0
            try: return float(val)
            except ValueError: return 0.0

        def safe_int(val):
            if not val: return 0
            try: return int(val)
            except ValueError: return 0

        new_payments = []
        for row in reader:
            payment = Payment(
                id=None,
                file_no=get_field(row, ['File_No', 'File No', 'Staff_ID']),
                name=get_field(row, 'Name'),
                conraiss=get_field(row, 'Conraiss'),
                amount_per_night=safe_float(get_field(row, ['Amt_per_night', 'Amount_per_night'])),
                dta=safe_float(get_field(row, 'DTA')),
                transport=safe_float(get_field(row, 'Transport')),
                numb_of_nights=safe_int(get_field(row, ['Numb_of_nights', 'Number_of_nights'])),
                total=safe_float(get_field(row, 'Total')),
                total_netpay=safe_float(get_field(row, ['Total_Netpay', 'Netpay'])),
                payment_title=get_field(row, 'Payment_Title'),
                bank=get_field(row, 'Bank'),
                account_numb=get_field(row, ['Account_Numb', 'Account_Number', 'Account_No', 'Account No']),
                tax=safe_float(get_field(row, 'Tax')),
                fuel_local=safe_float(get_field(row, ['Fuel-Local', 'Fuel_Local', 'Fuel Local', 'Local_Runs', 'Local Runs'])),
                station=get_field(row, 'Station'),
                posting=get_field(row, 'Posting'),
                created_at=None
            )
            new_payments.append(payment)

        self.repository.bulk_save(new_payments)
        
        # Update staff posted status to 'Y' for all staff in the payment
        if self.staff_repository:
            for payment in new_payments:
                if payment.file_no:
                    self.staff_repository.update_posted_status_by_file_no(payment.file_no, "Y")
        
        return len(new_payments)

    def delete_all(self):
        self.repository.delete_all()
