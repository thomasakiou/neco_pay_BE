from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.infrastructure.database import engine, SessionLocal
from app.infrastructure import models
from app.infrastructure.user_repository import UserRepository
from app.application.auth.utils import get_password_hash
from app.domain.user import User

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables and seed admin user
    models.Base.metadata.create_all(bind=engine)
    
    # Seed admin user if not exists
    db = SessionLocal()
    try:
        user_repo = UserRepository(db)
        if not user_repo.exists("admin"):
            admin_user = User(
                id=None,
                username="admin",
                hashed_password=get_password_hash("admin123"),
                role="admin",
                active=True,
                created_at=None
            )
            user_repo.save(admin_user)
            print("✅ Admin user created: username='admin', password='admin123'")
        else:
            print("ℹ️  Admin user already exists")
    finally:
        db.close()
    
    yield
    
    # Shutdown (if needed)

app = FastAPI(title="Payment Manager API", lifespan=lifespan)

@app.get("/api/health")
def health():
    return {"status": "ok"}
    
# Import routers
from app.api.endpoints import payment, staff, bank, distance, parameter, posting, state, auth

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(payment.router, prefix="/payments", tags=["payments"])
app.include_router(staff.router, prefix="/staff", tags=["staff"])
app.include_router(bank.router, prefix="/banks", tags=["banks"])
app.include_router(distance.router, prefix="/distances", tags=["distances"])
app.include_router(parameter.router, prefix="/parameters", tags=["parameters"])
app.include_router(posting.router, prefix="/postings", tags=["postings"])
app.include_router(state.router, prefix="/states", tags=["states"])
