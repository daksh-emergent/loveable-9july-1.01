from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorCollection
import os
from typing import Optional, List, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.db = None
        
    async def connect(self):
        """Connect to MongoDB"""
        try:
            mongo_url = os.environ.get('MONGO_URL')
            if not mongo_url:
                raise ValueError("MONGO_URL environment variable is not set")
            
            self.client = AsyncIOMotorClient(mongo_url)
            self.db = self.client[os.environ.get('DB_NAME', 'test_database')]
            
            # Test the connection
            await self.client.admin.command('ping')
            logger.info("Connected to MongoDB successfully")
            
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    async def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB")
    
    async def get_collection(self, collection_name: str) -> AsyncIOMotorCollection:
        """Get a collection from the database"""
        if self.db is None:
            await self.connect()
        return self.db[collection_name]
    
    async def create_indexes(self):
        """Create necessary indexes for performance"""
        try:
            # Hero content indexes
            hero_collection = await self.get_collection("hero_content")
            await hero_collection.create_index([("is_active", 1)])
            
            # Features indexes
            features_collection = await self.get_collection("features")
            await features_collection.create_index([("is_active", 1), ("order", 1)])
            await features_collection.create_index([("category", 1)])
            
            # Testimonials indexes
            testimonials_collection = await self.get_collection("testimonials")
            await testimonials_collection.create_index([("is_active", 1), ("order", 1)])
            
            # Process steps indexes
            process_steps_collection = await self.get_collection("process_steps")
            await process_steps_collection.create_index([("is_active", 1), ("order", 1)])
            await process_steps_collection.create_index([("step_type", 1)])
            
            # Specifications indexes
            specifications_collection = await self.get_collection("specifications")
            await specifications_collection.create_index([("is_active", 1), ("order", 1)])
            
            # Navigation indexes
            navigation_collection = await self.get_collection("navigation")
            await navigation_collection.create_index([("is_active", 1), ("nav_type", 1), ("order", 1)])
            
            # Footer sections indexes
            footer_collection = await self.get_collection("footer_sections")
            await footer_collection.create_index([("is_active", 1), ("section_type", 1), ("order", 1)])
            
            # Newsletter indexes
            newsletter_collection = await self.get_collection("newsletter_signups")
            await newsletter_collection.create_index([("email", 1)], unique=True)
            await newsletter_collection.create_index([("created_at", -1)])
            
            # Site settings indexes
            site_settings_collection = await self.get_collection("site_settings")
            await site_settings_collection.create_index([("is_active", 1)])
            
            # Content pages indexes
            content_pages_collection = await self.get_collection("content_pages")
            await content_pages_collection.create_index([("slug", 1)], unique=True)
            await content_pages_collection.create_index([("published", 1), ("page_type", 1)])
            
            # Page views indexes
            page_views_collection = await self.get_collection("page_views")
            await page_views_collection.create_index([("timestamp", -1)])
            await page_views_collection.create_index([("page_path", 1)])
            
            # Contact forms indexes
            contact_forms_collection = await self.get_collection("contact_forms")
            await contact_forms_collection.create_index([("created_at", -1)])
            await contact_forms_collection.create_index([("status", 1)])
            
            logger.info("Database indexes created successfully")
            
        except Exception as e:
            logger.error(f"Failed to create indexes: {e}")
            raise

# Global database manager instance
db_manager = DatabaseManager()

# Helper functions for common database operations
async def get_all_documents(collection_name: str, filter_dict: Dict[str, Any] = None, 
                          sort_field: str = "order", sort_direction: int = 1, 
                          limit: int = 1000) -> List[Dict[str, Any]]:
    """Get all documents from a collection with optional filtering and sorting"""
    collection = await db_manager.get_collection(collection_name)
    filter_dict = filter_dict or {"is_active": True}
    
    cursor = collection.find(filter_dict).sort(sort_field, sort_direction).limit(limit)
    documents = await cursor.to_list(length=limit)
    
    # Convert ObjectId to string
    for doc in documents:
        if '_id' in doc:
            doc['_id'] = str(doc['_id'])
    
    return documents

async def get_document_by_id(collection_name: str, document_id: str) -> Optional[Dict[str, Any]]:
    """Get a single document by ID"""
    collection = await db_manager.get_collection(collection_name)
    doc = await collection.find_one({"id": document_id})
    
    # Convert ObjectId to string
    if doc and '_id' in doc:
        doc['_id'] = str(doc['_id'])
    
    return doc

async def create_document(collection_name: str, document: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new document"""
    collection = await db_manager.get_collection(collection_name)
    document["created_at"] = datetime.utcnow()
    document["updated_at"] = datetime.utcnow()
    
    result = await collection.insert_one(document)
    if result.inserted_id:
        doc = await collection.find_one({"_id": result.inserted_id})
        if doc and '_id' in doc:
            doc['_id'] = str(doc['_id'])
        return doc
    return document

async def update_document(collection_name: str, document_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Update a document by ID"""
    collection = await db_manager.get_collection(collection_name)
    update_data["updated_at"] = datetime.utcnow()
    
    result = await collection.update_one(
        {"id": document_id},
        {"$set": update_data}
    )
    
    if result.modified_count > 0:
        doc = await collection.find_one({"id": document_id})
        if doc and '_id' in doc:
            doc['_id'] = str(doc['_id'])
        return doc
    return None

async def delete_document(collection_name: str, document_id: str) -> bool:
    """Delete a document by ID (soft delete by setting is_active to False)"""
    collection = await db_manager.get_collection(collection_name)
    result = await collection.update_one(
        {"id": document_id},
        {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
    )
    return result.modified_count > 0

async def search_documents(collection_name: str, search_query: str, 
                         search_fields: List[str] = None) -> List[Dict[str, Any]]:
    """Search documents using text search"""
    collection = await db_manager.get_collection(collection_name)
    search_fields = search_fields or ["title", "description", "content"]
    
    # Create text search query
    or_conditions = []
    for field in search_fields:
        or_conditions.append({field: {"$regex": search_query, "$options": "i"}})
    
    filter_dict = {
        "$and": [
            {"is_active": True},
            {"$or": or_conditions}
        ]
    }
    
    cursor = collection.find(filter_dict).sort("order", 1)
    return await cursor.to_list(length=1000)