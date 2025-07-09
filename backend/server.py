from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List
import uuid
from datetime import datetime

# Import our new content API and cache
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
import content_api
from content_api import router as content_router
from database import db_manager
from cache import cache_manager


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create the main app without a prefix
app = FastAPI(title="Atlas Robot API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Define Models for existing status check endpoints
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

# Existing status check endpoints
@api_router.get("/")
async def root():
    return {"message": "Atlas Robot API v1.0.0 - Backend is running"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    collection = await db_manager.get_collection("status_checks")
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    await collection.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    collection = await db_manager.get_collection("status_checks")
    status_checks = await collection.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

# Include content API routes
api_router.include_router(content_router, prefix="/content")

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    """Initialize database connection and create indexes"""
    try:
        await db_manager.connect()
        await db_manager.create_indexes()
        logger.info("Database connection established and indexes created")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection"""
    await db_manager.disconnect()
    logger.info("Database connection closed")
