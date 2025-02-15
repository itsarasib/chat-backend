from fastapi import FastAPI
from auth import auth_router
from completion import completion_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router.router)
app.include_router(completion_router.router)


@app.get("/")
def root():
    return {"message": "FastAPI + PostgreSQL + SQLAlchemy + Alembic"}
