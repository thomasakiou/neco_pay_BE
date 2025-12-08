from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class StaffBase(BaseModel):
    staff_id: str
    surname: str
    firstname: str
    middlename: Optional[str] = None
    res: Optional[str] = None
    tcheck: Optional[str] = None
    dup: Optional[str] = None
    dcode: Optional[str] = None
    name1: Optional[str] = None
    name: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None
    state: Optional[str] = None
    div: Optional[str] = None
    union: Optional[str] = None
    post: Optional[str] = None
    status: Optional[str] = None
    posted: Optional[str] = None
    bank: Optional[str] = None
    tt: Optional[str] = None
    mcs_no: Optional[str] = None
    ippis: Optional[str] = None
    title: Optional[str] = None
    s_origin: Optional[str] = None
    t_origin: Optional[str] = None
    local_gov: Optional[str] = None
    rank: Optional[str] = None
    rank2: Optional[str] = None
    rank3: Optional[str] = None
    contiss: Optional[str] = None
    level: Optional[str] = None
    step: Optional[str] = None
    oldcontiss: Optional[str] = None
    oldstep: Optional[str] = None
    sal_annum: Optional[float] = None
    bank_code: Optional[str] = None
    sortcode: Optional[str] = None
    bank_name: Optional[str] = None
    bank_locat: Optional[str] = None
    account_no: Optional[str] = None
    old_acct: Optional[str] = None
    branch: Optional[str] = None
    eff_date: Optional[date] = None
    daterecall: Optional[date] = None
    datestoppe: Optional[date] = None
    remark: Optional[str] = None
    reason: Optional[str] = None
    mvariation: Optional[str] = None
    group_code: Optional[str] = None
    active: bool = True

class CreateStaffDTO(StaffBase):
    pass

class UpdateStaffDTO(StaffBase):
    pass

class StaffDTO(StaffBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
