from typing import List, IO
import pandas as pd
import tempfile
import os
from dbfread import DBF
from datetime import datetime as dt
from sqlalchemy.orm import Session
from fastapi import UploadFile

from app.domain.staff import Staff
from app.infrastructure.repository import StaffRepository

class StaffService:
    def __init__(self, repository: StaffRepository):
        self.repository = repository

    async def process_upload(self, file: UploadFile):
        filename = file.filename
        content = await file.read()
        
        # Save to temp file to handle DBF reading which usually requires a path
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
                table = DBF(tmp_path, encoding='cp1252', char_decode_errors='ignore') # Encoding fallback
                data = [dict(record) for record in table]
            else:
                raise ValueError("Unsupported file format")

            staff_list = []
            for row in data:
                # Normalization
                # Replace nan with None
                row = {k: (None if pd.isna(v) else v) for k, v in row.items()}
                
                # Map fields. Assuming headers match DBF column names (case insensitive maybe?)
                # For now, simplistic mapping based on exact names or lower case
                
                # Helper to get value case-insensitively
                def get_val(key):
                    # Check upper, lower, title
                    for k in [key, key.upper(), key.lower()]:
                        if k in row:
                            return row[k]
                    return None

                # Handle Dates
                # DBF dates come as Date objects. CSV/Excel might be strings.
                def parse_date(v):
                    if not v: return None
                    if isinstance(v, (dt, pd.Timestamp)): return v.date() # If it's already a date/datetime
                    # Attempt parse string
                    try:
                        return pd.to_datetime(v).date()
                    except:
                        return None
                
                staff = Staff(
                    id=None, # Auto-gen
                    staff_id=str(get_val('PER_NO') or get_val('staff_id')),
                    surname=str(get_val('SURNAME') or ''),
                    firstname=str(get_val('FIRSTNAME') or ''),
                    middlename=str(get_val('MIDDLENAME')),
                    res=get_val('RES'),
                    tcheck=get_val('TCHECK'),
                    dup=get_val('DUP'),
                    dcode=get_val('DCODE'),
                    name1=get_val('NAME1'),
                    name=get_val('NAME'),
                    department=get_val('DEPARTMENT'),
                    location=get_val('LOCATION'),
                    state=get_val('STATE'),
                    div=get_val('DIV'),
                    union=get_val('UNION'),
                    post=get_val('POST'),
                    status=get_val('STATUS'),
                    posted=get_val('POSTED'),
                    bank=get_val('BANK'),
                    tt=get_val('TT'),
                    mcs_no=get_val('MCS_NO'),
                    ippis=get_val('IPPIS'),
                    title=get_val('TITLE'),
                    s_origin=get_val('S_ORIGIN'),
                    t_origin=get_val('T_ORIGIN'),
                    local_gov=get_val('LOCAL_GOV'),
                    rank=get_val('RANK'),
                    rank2=get_val('RANK2'),
                    rank3=get_val('RANK3'),
                    contiss=get_val('CONTISS'),
                    level=get_val('LEVEL'),
                    step=get_val('STEP'),
                    oldcontiss=get_val('OLDCONTISS'),
                    oldstep=get_val('OLDSTEP'),
                    sal_annum=float(get_val('SAL_ANNUM')) if get_val('SAL_ANNUM') else None,
                    bank_code=get_val('BANK_CODE'),
                    sortcode=get_val('SORTCODE'),
                    bank_name=get_val('BANK_NAME'),
                    bank_locat=get_val('BANK_LOCAT'),
                    account_no=get_val('ACCOUNT_NO'),
                    old_acct=get_val('OLD_ACCT'),
                    branch=get_val('BRANCH'),
                    eff_date=parse_date(get_val('EFF_DATE')),
                    daterecall=parse_date(get_val('DATERECALL')),
                    datestoppe=parse_date(get_val('DATESTOPPE')),
                    remark=get_val('REMARK'),
                    reason=get_val('REASON'),
                    mvariation=get_val('MVARIATION'),
                    group_code=get_val('GROUP'),

                    active=False if str(get_val('REMARK') or '').lower() == 'stop' else True,
                    created_at=None
                )
                
                if staff.staff_id and staff.staff_id != 'None':
                    staff_list.append(staff)

            self.repository.bulk_save(staff_list)
            return len(staff_list)

        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
