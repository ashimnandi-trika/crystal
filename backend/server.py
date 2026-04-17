from fastapi import FastAPI, APIRouter, Query
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List
import uuid
from datetime import datetime, timezone


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection with safe defaults
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
db_name = os.environ.get('DB_NAME', 'crystal_db')

if not mongo_url:
    logging.error("MONGO_URL is not set. Please configure it in backend/.env")

client = AsyncIOMotorClient(mongo_url)
db = client[db_name]

# Create the main app
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# CORS — restricted defaults
cors_origins = os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(',')
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=[o.strip() for o in cors_origins],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Define Models
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str


@api_router.get("/")
async def root():
    return {"message": "Crystal API"}


@api_router.get("/health")
async def health_check():
    """Health endpoint for load balancer checks."""
    try:
        await db.command("ping")
        return {"status": "ok", "database": "connected"}
    except Exception:
        return {"status": "degraded", "database": "disconnected"}


@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    try:
        status_dict = input.model_dump()
        status_obj = StatusCheck(**status_dict)

        doc = status_obj.model_dump()
        doc['timestamp'] = doc['timestamp'].isoformat()

        await db.status_checks.insert_one(doc)
        return status_obj
    except Exception as e:
        logger.error(f"Failed to create status check: {e}")
        return {"error": "Failed to create status check", "detail": str(e)}


@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=500),
):
    try:
        status_checks = await db.status_checks.find(
            {}, {"_id": 0}
        ).skip(skip).limit(limit).to_list(limit)

        for check in status_checks:
            if isinstance(check.get('timestamp'), str):
                check['timestamp'] = datetime.fromisoformat(check['timestamp'])

        return status_checks
    except Exception as e:
        logger.error(f"Failed to get status checks: {e}")
        return []


# Include the router
app.include_router(api_router)


@app.on_event("startup")
async def startup():
    try:
        await db.command("ping")
        logger.info(f"Connected to MongoDB: {db_name}")
    except Exception as e:
        logger.error(f"MongoDB connection failed: {e}")


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
