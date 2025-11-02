import os
from typing import Any, Dict, List, Optional

from pymongo import MongoClient
from pymongo.database import Database

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "app")

_client: MongoClient | None = None
_db: Database | None = None


def get_client() -> MongoClient:
    global _client
    if _client is None:
        _client = MongoClient(DATABASE_URL)
    return _client


def get_db() -> Database:
    global _db
    if _db is None:
        _db = get_client()[DATABASE_NAME]
    return _db

# Public handle
db = get_db()


def create_document(collection_name: str, data: Dict[str, Any]) -> str:
    from datetime import datetime

    payload = {**data, "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()}
    result = db[collection_name].insert_one(payload)
    return str(result.inserted_id)


def get_documents(
    collection_name: str,
    filter_dict: Optional[Dict[str, Any]] = None,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    cursor = db[collection_name].find(filter_dict or {}).limit(limit)
    docs: List[Dict[str, Any]] = []
    for doc in cursor:
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])
        docs.append(doc)
    return docs
