from typing import List
import pandas as pd
import tempfile
import os
from dbfread import DBF
from fastapi import UploadFile

from app.domain.distance import Distance
from app.infrastructure.repository import DistanceRepository

class DistanceService:
    def __init__(self, repository: DistanceRepository):
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

            distance_list = []
            for row in data:
                # Normalization
                row = {k: (None if pd.isna(v) else v) for k, v in row.items()}
                
                def get_val(key):
                    for k in [key, key.upper(), key.lower()]:
                        if k in row:
                            return row[k]
                    return None
                 
                # Schema: PCODE, SOURCE, TCODE, TARGET, DISTANCE, TSTATE
                
                dist_val = get_val('DISTANCE')
                if dist_val is not None:
                    try:
                        dist_val = float(dist_val)
                    except:
                        dist_val = 0.0

                distance = Distance(
                    id=None,
                    pcode=str(get_val('PCODE') or get_val('pcode')),
                    source=str(get_val('SOURCE') or get_val('source')),
                    tcode=str(get_val('TCODE') or get_val('tcode')),
                    target=str(get_val('TARGET') or get_val('target')),
                    distance=dist_val,
                    tstate=str(get_val('TSTATE') or get_val('tstate')),
                    active=True,
                    created_at=None
                )
                
                if distance.pcode or distance.source:
                     distance_list.append(distance)

            self.repository.bulk_save(distance_list)
            return len(distance_list)

        finally:
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except:
                    pass
