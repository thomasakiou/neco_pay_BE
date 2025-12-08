from fastapi import FastAPI
from app.infrastructure.database import engine
from app.infrastructure import models
from app.api.endpoints import payment, staff

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Payment Manager API")

app.include_router(payment.router, prefix="/payments", tags=["payments"])
app.include_router(staff.router, prefix="/staff", tags=["staff"])

from app.api.endpoints import payment, staff, bank

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Payment Manager API")

app.include_router(payment.router, prefix="/payments", tags=["payments"])
app.include_router(staff.router, prefix="/staff", tags=["staff"])
app.include_router(bank.router, prefix="/banks", tags=["banks"])

from app.api.endpoints import distance
app.include_router(distance.router, prefix="/distances", tags=["distances"])

from app.api.endpoints import parameter
app.include_router(parameter.router, prefix="/parameters", tags=["parameters"])

from app.api.endpoints import posting
app.include_router(posting.router, prefix="/postings", tags=["postings"])

from app.api.endpoints import state
app.include_router(state.router, prefix="/states", tags=["states"])
