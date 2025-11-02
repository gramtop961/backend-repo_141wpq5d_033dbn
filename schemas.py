from pydantic import BaseModel, Field
from typing import Optional

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
    collections: list[str] = []
