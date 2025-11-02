from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from schemas import HealthResponse
from database import db

app = FastAPI(title="Brixel API", version="0.1.0")

# CORS - allow all for sandbox; in production, restrict to frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Brixel backend is live"}


@app.get("/test", response_model=HealthResponse)
async def test_db():
    database_url = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
    database_name = os.getenv("DATABASE_NAME", "app")

    try:
        collections = db.list_collection_names()
        status = "connected"
    except Exception as e:
        collections = []
        status = f"error: {type(e).__name__}"

    return HealthResponse(
        backend="fastapi",
        database="mongodb",
        database_url=database_url,
        database_name=database_name,
        connection_status=status,
        collections=collections,
    )
