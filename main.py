from fastapi import FastAPI
from auth import auth_router

app = FastAPI()

# Include routers
app.include_router(auth_router.router)


@app.get("/")
def root():
    return {"message": "FastAPI + PostgreSQL + SQLAlchemy + Alembic"}
