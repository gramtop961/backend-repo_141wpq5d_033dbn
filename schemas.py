from pydantic import BaseModel, Field
from typing import Optional, List

# Example schema: each class typically maps to a collection named by its lowercase class name
class User(BaseModel):
    email: str
    name: str
    role: str = Field(default="worker")


class HealthResponse(BaseModel):
    backend: str
    database: str
    database_url: str
    database_name: str
    connection_status: str
    collections: List[str] = []


# --- Domain Schemas ---
class JobRequest(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    project_type: str
    description: Optional[str] = None
    budget: Optional[float] = None
    location: Optional[str] = None


class JobRequestResponse(BaseModel):
    id: str
    message: str


class KYCSubmission(BaseModel):
    full_name: str
    license_number: str
    issuing_state: Optional[str] = None
    document_url: Optional[str] = None


class KYCStatus(BaseModel):
    id: str
    status: str = Field(description="verification status: pending, verified, or failed")
    reason: Optional[str] = None
