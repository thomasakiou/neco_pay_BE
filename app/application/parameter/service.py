from typing import List
import pandas as pd
import tempfile
import os
from dbfread import DBF
from fastapi import UploadFile

from app.domain.parameter import Parameter
from app.infrastructure.repository import ParameterRepository

class ParameterService:
    def __init__(self, repository: ParameterRepository):
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

            parameter_list = []
            for row in data:
                row = {k: (None if pd.isna(v) else v) for k, v in row.items()}
                
                def get_val(key):
                    for k in [key, key.upper(), key.lower()]:
                        if k in row:
                            return row[k]
                    return None
                 
                # Schema: CONTISS, PERNIGHT, LOCAL, KILOMETER
                
                def get_float(k):
                    v = get_val(k)
                    if v is not None:
                        try:
                            return float(v)
                        except:
                            return 0.0
                    return None

                parameter = Parameter(
                    id=None,
                    contiss=str(get_val('CONTISS') or get_val('contiss')),
                    pernight=get_float('PERNIGHT'),
                    local=get_float('LOCAL'),
                    kilometer=get_float('KILOMETER'),
                    active=True,
                    created_at=None
                )
                
                if parameter.contiss:
                     parameter_list.append(parameter)

            self.repository.bulk_save(parameter_list)
            return len(parameter_list)

        finally:
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except:
                    pass
