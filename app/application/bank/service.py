from typing import List
import pandas as pd
import tempfile
import os
from dbfread import DBF
from fastapi import UploadFile

from app.domain.bank import Bank
from app.infrastructure.repository import BankRepository

class BankService:
    def __init__(self, repository: BankRepository):
        self.repository = repository

    async def process_upload(self, file: UploadFile) -> int:
        filename = file.filename
        content = await file.read()
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        try:
            data = []
            if filename.lower().endswith('.csv'):
                df = pd.read_csv(tmp_path)
                data = df.to_dict('records')
            elif filename.lower().endswith('.xlsx'):
                df = pd.read_excel(tmp_path)
                data = df.to_dict('records')
            elif filename.lower().endswith('.dbf'):
                table = DBF(tmp_path, encoding='cp1252', char_decode_errors='ignore')
                data = [dict(record) for record in table]
            else:
                raise ValueError("Unsupported file format")

            bank_list = []
            for row in data:
                # Normalization
                row = {k: (None if pd.isna(v) else v) for k, v in row.items()}
                
                def get_val(key):
                    for k in [key, key.upper(), key.lower()]:
                        if k in row:
                            return row[k]
                    return None

                # Mapping based on DBF schema
                # CODE, BNAME, SORTCODE, BRANCH, BLOCATION
                
                bank = Bank(
                    id=None,
                    code=str(get_val('CODE') or get_val('code')),
                    name=str(get_val('BNAME') or get_val('name')),
                    sort_code=str(get_val('SORTCODE') or get_val('sort_code')),
                    branch=str(get_val('BRANCH') or get_val('branch')),
                    location=str(get_val('BLOCATION') or get_val('location')),
                    active=True, # Default to True
                    created_at=None
                )
                
                # Basic validation: ensure at least code or name exists
                if bank.code or bank.name:
                     bank_list.append(bank)

            self.repository.bulk_save(bank_list)
            return len(bank_list)

        finally:
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except:
                    pass
