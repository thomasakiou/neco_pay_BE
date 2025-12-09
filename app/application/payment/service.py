from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.payment import Payment
from app.infrastructure.repository import PaymentRepository
from app.infrastructure.models import PostingModel, StaffModel, ParameterModel, DistanceModel

class PaymentService:
    def __init__(self, repository: PaymentRepository, db: Session):
        self.repository = repository
        self.db = db

    def upload_payments(self, file_content: str) -> int:
        import csv
        from io import StringIO
        
        f = StringIO(file_content)
        reader = csv.DictReader(f)
        
        # CSV Headers: File_No,Name,Conraiss,Amt_per_night,DTA,Transport,Numb_of_nights,Total,Total_Netpay,Payment_Title
        # Map to Payment Model:
        # File_No -> file_no
        # Name -> name
        # Conraiss -> conraiss
        # Amt_per_night -> amount_per_night
        # DTA -> dta
        # Transport -> transport
        # Numb_of_nights -> numb_of_nights
        # Total -> total
        # Total_Netpay -> total_netpay
        # Payment_Title -> payment_title
        
        new_payments = []
        for row in reader:
            # Handle potential empty strings or missing fields gracefully
            def safe_float(val):
                if not val: return 0.0
                try: return float(val)
                except ValueError: return 0.0

            def safe_int(val):
                if not val: return 0
                try: return int(val)
                except ValueError: return 0

            payment = Payment(
                id=None,
                file_no=row.get('File_No'),
                name=row.get('Name'),
                conraiss=row.get('Conraiss'),
                amount_per_night=safe_float(row.get('Amt_per_night')),
                dta=safe_float(row.get('DTA')),
                transport=safe_float(row.get('Transport')),
                numb_of_nights=safe_int(row.get('Numb_of_nights')),
                total=safe_float(row.get('Total')),
                total_netpay=safe_float(row.get('Total_Netpay')),
                payment_title=row.get('Payment_Title'),
                bank=row.get('Bank'),
                account_numb=row.get('Account_Numb'),
                tax=safe_float(row.get('Tax')),
                fuel_local=safe_float(row.get('Fuel-Local') or row.get('Fuel_Local')), 
                station=row.get('Station'),
                posting=row.get('Posting'),
                created_at=None
            )
            new_payments.append(payment)

        self.repository.bulk_save(new_payments)
        return len(new_payments)

    def delete_all(self):
        self.repository.delete_all()
