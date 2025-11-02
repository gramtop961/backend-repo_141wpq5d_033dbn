from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os

from schemas import HealthResponse, JobRequest, JobRequestResponse, KYCSubmission, KYCStatus
from database import db, create_document, get_documents

app = FastAPI(title="Brixel API", version="0.2.0")

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


# --- Job Requests ---
@app.post("/jobs/request", response_model=JobRequestResponse)
async def create_job_request(payload: JobRequest):
    data = payload.dict()
    doc_id = create_document("jobrequest", data)
    return JobRequestResponse(id=doc_id, message="Job request received. We'll be in touch soon.")


@app.get("/jobs")
async def list_job_requests(limit: int = 50):
    docs = get_documents("jobrequest", limit=limit)
    return {"items": docs}


# --- KYC / License Verification (stubs) ---
@app.post("/kyc/verify", response_model=KYCStatus)
async def submit_kyc(payload: KYCSubmission):
    # Store submission with pending status. In real life we would call an external provider.
    record = {**payload.dict(), "status": "pending"}
    doc_id = create_document("kycsubmission", record)
    return KYCStatus(id=doc_id, status="pending")


@app.get("/kyc", response_model=list[KYCStatus])
async def list_kyc(limit: int = 50):
    items = get_documents("kycsubmission", limit=limit)
    # Normalize to KYCStatus shape
    statuses = []
    for it in items:
        statuses.append(KYCStatus(id=it.get("_id", ""), status=it.get("status", "pending"), reason=it.get("reason")))
    return statuses
