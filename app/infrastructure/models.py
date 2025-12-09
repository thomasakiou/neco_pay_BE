from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from app.domain.payment import Payment
from app.domain.user import User

Base = declarative_base()

class PaymentModel(Base):
    __tablename__ = "payment"

    id = Column(Integer, primary_key=True, index=True)
    
    file_no = Column(String, nullable=True)     # File_No
    name = Column(String, nullable=True)        # Name
    conraiss = Column(String, nullable=True)    # Conraiss
    amount_per_night = Column(Float, nullable=True) # Amt_per_night
    dta = Column(Float, nullable=True)          # DTA
    transport = Column(Float, nullable=True)    # Transport
    numb_of_nights = Column(Integer, nullable=True) # Numb_of_nights
    total = Column(Float, nullable=True)        # Total
    total_netpay = Column(Float, nullable=True) # Total_Netpay
    payment_title = Column(String, nullable=True) # Payment_Title
    
    bank = Column(String, nullable=True)        # Bank
    account_numb = Column(String, nullable=True)# Account_Numb
    tax = Column(Float, nullable=True)          # Tax
    fuel_local = Column(Float, nullable=True)   # Fuel-Local
    station = Column(String, nullable=True)     # Station
    posting = Column(String, nullable=True)     # Posting

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_entity(self) -> Payment:
        return Payment(
            id=self.id,
            file_no=self.file_no,
            name=self.name,
            conraiss=self.conraiss,
            amount_per_night=self.amount_per_night,
            dta=self.dta,
            transport=self.transport,
            numb_of_nights=self.numb_of_nights,
            total=self.total,
            total_netpay=self.total_netpay,
            payment_title=self.payment_title,
            bank=self.bank,
            account_numb=self.account_numb,
            tax=self.tax,
            fuel_local=self.fuel_local,

            station=self.station,
            posting=self.posting,
            created_at=self.created_at
        )

    @staticmethod
    def from_entity(payment: Payment) -> "PaymentModel":
        return PaymentModel(
            id=payment.id,
            file_no=payment.file_no,
            name=payment.name,
            conraiss=payment.conraiss,
            amount_per_night=payment.amount_per_night,
            dta=payment.dta,
            transport=payment.transport,
            numb_of_nights=payment.numb_of_nights,
            total=payment.total,
            total_netpay=payment.total_netpay,
            payment_title=payment.payment_title,
            bank=payment.bank,
            account_numb=payment.account_numb,
            tax=payment.tax,
            fuel_local=payment.fuel_local,

            station=payment.station,
            posting=payment.posting,
            created_at=payment.created_at
        )

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="admin")
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_entity(self) -> User:
        return User(
            id=self.id,
            username=self.username,
            hashed_password=self.hashed_password,
            role=self.role,
            active=self.active,
            created_at=self.created_at
        )

    @staticmethod
    def from_entity(user: User) -> "UserModel":
        return UserModel(
            id=user.id,
            username=user.username,
            hashed_password=user.hashed_password,
            role=user.role,
            active=user.active,
            created_at=user.created_at
        )

from app.domain.staff import Staff
from sqlalchemy import Date

class StaffModel(Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True, index=True)
    staff_id = Column(String, unique=True, index=True) # PER_NO
    
    # Mapping DBF fields
    res = Column(String, nullable=True)
    tcheck = Column(String, nullable=True)
    dup = Column(String, nullable=True)
    dcode = Column(String, nullable=True)
    per_no = Column(String, nullable=True) # Keeping original name too? No, mapped to staff_id
    name1 = Column(String, nullable=True)
    name = Column(String, nullable=True)
    department = Column(String, nullable=True)
    location = Column(String, nullable=True)
    state = Column(String, nullable=True)
    div = Column(String, nullable=True)
    union_val = Column(String, name="union", nullable=True) # UNION is keyword
    post = Column(String, nullable=True)
    status = Column(String, nullable=True)
    posted = Column(String, nullable=True)
    bank = Column(String, nullable=True)
    tt = Column(String, nullable=True)
    mcs_no = Column(String, nullable=True)
    ippis = Column(String, nullable=True)
    title = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    firstname = Column(String, nullable=True)
    middlename = Column(String, nullable=True)
    s_origin = Column(String, nullable=True)
    t_origin = Column(String, nullable=True)
    local_gov = Column(String, nullable=True)
    rank = Column(String, nullable=True)
    rank2 = Column(String, nullable=True)
    rank3 = Column(String, nullable=True)
    contiss = Column(String, nullable=True)
    level = Column(String, nullable=True)
    step = Column(String, nullable=True)
    oldcontiss = Column(String, nullable=True)
    oldstep = Column(String, nullable=True)
    sal_annum = Column(Float, nullable=True)
    bank_code = Column(String, nullable=True)
    sortcode = Column(String, nullable=True)
    bank_name = Column(String, nullable=True)
    bank_locat = Column(String, nullable=True)
    account_no = Column(String, nullable=True)
    old_acct = Column(String, nullable=True)
    branch = Column(String, nullable=True)
    eff_date = Column(Date, nullable=True)
    daterecall = Column(Date, nullable=True)
    datestoppe = Column(Date, nullable=True)
    remark = Column(String, nullable=True)
    reason = Column(String, nullable=True)
    mvariation = Column(String, nullable=True)
    group_code = Column(String, name="group", nullable=True) # GROUP is keyword
    active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_entity(self) -> Staff:
        return Staff(
            id=self.id,
            staff_id=self.staff_id,
            surname=self.surname,
            firstname=self.firstname,
            middlename=self.middlename,
            res=self.res,
            tcheck=self.tcheck,
            dup=self.dup,
            dcode=self.dcode,
            name1=self.name1,
            name=self.name,
            department=self.department,
            location=self.location,
            state=self.state,
            div=self.div,
            union=self.union_val,
            post=self.post,
            status=self.status,
            posted=self.posted,
            bank=self.bank,
            tt=self.tt,
            mcs_no=self.mcs_no,
            ippis=self.ippis,
            title=self.title,
            s_origin=self.s_origin,
            t_origin=self.t_origin,
            local_gov=self.local_gov,
            rank=self.rank,
            rank2=self.rank2,
            rank3=self.rank3,
            contiss=self.contiss,
            level=self.level,
            step=self.step,
            oldcontiss=self.oldcontiss,
            oldstep=self.oldstep,
            sal_annum=self.sal_annum,
            bank_code=self.bank_code,
            sortcode=self.sortcode,
            bank_name=self.bank_name,
            bank_locat=self.bank_locat,
            account_no=self.account_no,
            old_acct=self.old_acct,
            branch=self.branch,
            eff_date=self.eff_date,
            daterecall=self.daterecall,
            datestoppe=self.datestoppe,
            remark=self.remark,
            reason=self.reason,
            mvariation=self.mvariation,
            group_code=self.group_code,
            active=self.active,
            created_at=self.created_at
        )

    @staticmethod
    def from_entity(staff: Staff) -> "StaffModel":
        return StaffModel(
            id=staff.id,
            staff_id=staff.staff_id,
            surname=staff.surname,
            firstname=staff.firstname,
            middlename=staff.middlename,
            res=staff.res,
            tcheck=staff.tcheck,
            dup=staff.dup,
            dcode=staff.dcode,
            name1=staff.name1,
            name=staff.name,
            department=staff.department,
            location=staff.location,
            state=staff.state,
            div=staff.div,
            union_val=staff.union,
            post=staff.post,
            status=staff.status,
            posted=staff.posted,
            bank=staff.bank,
            tt=staff.tt,
            mcs_no=staff.mcs_no,
            ippis=staff.ippis,
            title=staff.title,
            s_origin=staff.s_origin,
            t_origin=staff.t_origin,
            local_gov=staff.local_gov,
            rank=staff.rank,
            rank2=staff.rank2,
            rank3=staff.rank3,
            contiss=staff.contiss,
            level=staff.level,
            step=staff.step,
            oldcontiss=staff.oldcontiss,
            oldstep=staff.oldstep,
            sal_annum=staff.sal_annum,
            bank_code=staff.bank_code,
            sortcode=staff.sortcode,
            bank_name=staff.bank_name,
            bank_locat=staff.bank_locat,
            account_no=staff.account_no,
            old_acct=staff.old_acct,
            branch=staff.branch,
            eff_date=staff.eff_date,
            daterecall=staff.daterecall,
            datestoppe=staff.datestoppe,
            remark=staff.remark,
            reason=staff.reason,
            mvariation=staff.mvariation,
            group_code=staff.group_code,
            active=staff.active,
            created_at=staff.created_at
        )

from app.domain.bank import Bank

class BankModel(Base):
    __tablename__ = "bank"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=True)     # From CODE
    name = Column(String, nullable=True)     # From BNAME
    sort_code = Column(String, nullable=True)# From SORTCODE
    branch = Column(String, nullable=True)   # From BRANCH
    location = Column(String, nullable=True) # From BLOCATION
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_entity(self) -> Bank:
        return Bank(
            id=self.id,
            code=self.code,
            name=self.name,
            sort_code=self.sort_code,
            branch=self.branch,
            location=self.location,
            active=self.active,
            created_at=self.created_at
        )

    @staticmethod
    def from_entity(bank: Bank) -> "BankModel":
        return BankModel(
            id=bank.id,
            code=bank.code,
            name=bank.name,
            sort_code=bank.sort_code,
            branch=bank.branch,
            location=bank.location,
            active=bank.active,
            created_at=bank.created_at
        )

from app.domain.distance import Distance

class DistanceModel(Base):
    __tablename__ = "distance"

    id = Column(Integer, primary_key=True, index=True)
    pcode = Column(String, nullable=True)
    source = Column(String, nullable=True)
    tcode = Column(String, nullable=True)
    target = Column(String, nullable=True)
    distance = Column(Float, nullable=True)
    tstate = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_entity(self) -> Distance:
        return Distance(
            id=self.id,
            pcode=self.pcode,
            source=self.source,
            tcode=self.tcode,
            target=self.target,
            distance=self.distance,
            tstate=self.tstate,
            active=self.active,
            created_at=self.created_at
        )

    @staticmethod
    def from_entity(distance: Distance) -> "DistanceModel":
        return DistanceModel(
            id=distance.id,
            pcode=distance.pcode,
            source=distance.source,
            tcode=distance.tcode,
            target=distance.target,
            distance=distance.distance,
            tstate=distance.tstate,
            active=distance.active,
            created_at=distance.created_at
        )

from app.domain.parameter import Parameter

class ParameterModel(Base):
    __tablename__ = "parameter"

    id = Column(Integer, primary_key=True, index=True)
    contiss = Column(String, nullable=True)
    pernight = Column(Float, nullable=True)
    local = Column(Float, nullable=True)
    kilometer = Column(Float, nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_entity(self) -> Parameter:
        return Parameter(
            id=self.id,
            contiss=self.contiss,
            pernight=self.pernight,
            local=self.local,
            kilometer=self.kilometer,
            active=self.active,
            created_at=self.created_at
        )

    @staticmethod
    def from_entity(parameter: Parameter) -> "ParameterModel":
        return ParameterModel(
            id=parameter.id,
            contiss=parameter.contiss,
            pernight=parameter.pernight,
            local=parameter.local,
            kilometer=parameter.kilometer,
            active=parameter.active,
            created_at=parameter.created_at
        )

from app.domain.posting import Posting

class PostingModel(Base):
    __tablename__ = "posting"

    id = Column(Integer, primary_key=True, index=True)
    # state = Column(String, nullable=True)
    file_no = Column(String, nullable=True)
    name = Column(String, nullable=True)
    conraiss = Column(String, nullable=True)
    station = Column(String, nullable=True)
    posting = Column(String, nullable=True)
    # category = Column(String, nullable=True) # Unused
    # rank = Column(String, nullable=True) # Unused
    # mandate = Column(String, nullable=True) # Unused
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_entity(self) -> Posting:
        return Posting(
            id=self.id,
            # state=self.state,
            file_no=self.file_no,
            name=self.name,
            conraiss=self.conraiss,
            station=self.station,
            posting=self.posting,
            # category=self.category, # Fields from old CSV might be null now
            # rank=self.rank,
            # mandate=self.mandate,
            active=self.active,
            created_at=self.created_at
        )

    @staticmethod
    def from_entity(posting: Posting) -> "PostingModel":
        return PostingModel(
            id=posting.id,
            # state=posting.state,
            file_no=posting.file_no,
            name=posting.name,
            conraiss=posting.conraiss,
            station=posting.station,
            posting=posting.posting,
            # category=posting.category,
            # rank=posting.rank,
            # mandate=posting.mandate,
            active=posting.active,
            created_at=posting.created_at
        )

from app.domain.state import State

class StateModel(Base):
    __tablename__ = "state"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=True)
    state = Column(String, nullable=True)
    capital = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_entity(self) -> State:
        return State(
            id=self.id,
            code=self.code,
            state=self.state,
            capital=self.capital,
            active=self.active,
            created_at=self.created_at
        )

    @staticmethod
    def from_entity(state: State) -> "StateModel":
        return StateModel(
            id=state.id,
            code=state.code,
            state=state.state,
            capital=state.capital,
            active=state.active,
            created_at=state.created_at
        )
