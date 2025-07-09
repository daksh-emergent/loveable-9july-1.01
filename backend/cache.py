import redis
import json
import logging
from typing import Optional, Any, Dict, List
from datetime import datetime, timedelta
import os

logger = logging.getLogger(__name__)

class CacheManager:
    def __init__(self):
        self.redis_client = None
        self.cache_enabled = True
        self.default_ttl = 3600  # 1 hour default TTL
        
    def connect(self):
        """Connect to Redis"""
        try:
            # Use Redis if available, otherwise use in-memory cache
            redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379')
            self.redis_client = redis.from_url(redis_url, decode_responses=True)
            # Test connection
            self.redis_client.ping()
            logger.info("Connected to Redis successfully")
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}. Using in-memory cache fallback.")
            self.redis_client = InMemoryCache()
            
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.cache_enabled:
            return None
            
        try:
            if not self.redis_client:
                self.connect()
                
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Cache get error for key {key}: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache"""
        if not self.cache_enabled:
            return False
            
        try:
            if not self.redis_client:
                self.connect()
                
            ttl = ttl or self.default_ttl
            serialized_value = json.dumps(value, default=str)
            
            if hasattr(self.redis_client, 'setex'):
                # Redis client
                self.redis_client.setex(key, ttl, serialized_value)
            else:
                # In-memory cache
                self.redis_client.set(key, serialized_value, ttl)
            
            return True
        except Exception as e:
            logger.error(f"Cache set error for key {key}: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        if not self.cache_enabled:
            return False
            
        try:
            if not self.redis_client:
                self.connect()
                
            self.redis_client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Cache delete error for key {key}: {e}")
            return False
    
    def clear_pattern(self, pattern: str) -> int:
        """Clear all keys matching pattern"""
        if not self.cache_enabled:
            return 0
            
        try:
            if not self.redis_client:
                self.connect()
                
            if hasattr(self.redis_client, 'keys'):
                # Redis client
                keys = self.redis_client.keys(pattern)
                if keys:
                    return self.redis_client.delete(*keys)
            else:
                # In-memory cache
                return self.redis_client.clear_pattern(pattern)
            
            return 0
        except Exception as e:
            logger.error(f"Cache clear pattern error for pattern {pattern}: {e}")
            return 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        try:
            if not self.redis_client:
                self.connect()
                
            if hasattr(self.redis_client, 'info'):
                # Redis client
                info = self.redis_client.info()
                return {
                    "used_memory": info.get("used_memory_human", "N/A"),
                    "connected_clients": info.get("connected_clients", 0),
                    "total_commands_processed": info.get("total_commands_processed", 0),
                    "cache_hits": info.get("keyspace_hits", 0),
                    "cache_misses": info.get("keyspace_misses", 0)
                }
            else:
                # In-memory cache
                return self.redis_client.get_stats()
                
        except Exception as e:
            logger.error(f"Cache stats error: {e}")
            return {"error": str(e)}

class InMemoryCache:
    """Fallback in-memory cache when Redis is not available"""
    def __init__(self):
        self.cache = {}
        self.expiry = {}
        self.stats = {
            "hits": 0,
            "misses": 0,
            "sets": 0,
            "deletes": 0
        }
    
    def get(self, key: str) -> Optional[str]:
        """Get value from in-memory cache"""
        # Check if key exists and hasn't expired
        if key in self.cache:
            if key not in self.expiry or datetime.now() < self.expiry[key]:
                self.stats["hits"] += 1
                return self.cache[key]
            else:
                # Key has expired
                self.delete(key)
        
        self.stats["misses"] += 1
        return None
    
    def set(self, key: str, value: str, ttl: int):
        """Set value in in-memory cache"""
        self.cache[key] = value
        if ttl:
            self.expiry[key] = datetime.now() + timedelta(seconds=ttl)
        self.stats["sets"] += 1
    
    def delete(self, key: str):
        """Delete key from in-memory cache"""
        if key in self.cache:
            del self.cache[key]
        if key in self.expiry:
            del self.expiry[key]
        self.stats["deletes"] += 1
    
    def clear_pattern(self, pattern: str) -> int:
        """Clear keys matching pattern"""
        # Simple pattern matching (only supports * wildcard)
        if "*" in pattern:
            prefix = pattern.replace("*", "")
            keys_to_delete = [k for k in self.cache.keys() if k.startswith(prefix)]
        else:
            keys_to_delete = [k for k in self.cache.keys() if k == pattern]
        
        for key in keys_to_delete:
            self.delete(key)
        
        return len(keys_to_delete)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get in-memory cache statistics"""
        return {
            "cache_size": len(self.cache),
            "cache_hits": self.stats["hits"],
            "cache_misses": self.stats["misses"],
            "cache_sets": self.stats["sets"],
            "cache_deletes": self.stats["deletes"],
            "hit_rate": self.stats["hits"] / (self.stats["hits"] + self.stats["misses"]) if (self.stats["hits"] + self.stats["misses"]) > 0 else 0
        }

# Global cache manager instance
cache_manager = CacheManager()

# Cache key generators
def get_cache_key(prefix: str, identifier: str = "", **kwargs) -> str:
    """Generate cache key with prefix and optional identifier"""
    key_parts = [prefix]
    if identifier:
        key_parts.append(identifier)
    
    # Add any additional parameters
    for k, v in kwargs.items():
        key_parts.append(f"{k}:{v}")
    
    return ":".join(key_parts)

# Cache decorators and utilities
def cache_result(key_prefix: str, ttl: Optional[int] = None):
    """Decorator to cache function results"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = get_cache_key(key_prefix, **kwargs)
            
            # Try to get from cache first
            cached_result = cache_manager.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Call function and cache result
            result = await func(*args, **kwargs)
            if result is not None:
                cache_manager.set(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator

# Content-specific cache functions
async def get_cached_content(content_type: str, filters: Dict[str, Any] = None) -> Optional[List[Dict[str, Any]]]:
    """Get cached content by type"""
    cache_key = get_cache_key(f"content:{content_type}", **filters or {})
    return cache_manager.get(cache_key)

async def set_cached_content(content_type: str, content: List[Dict[str, Any]], 
                           filters: Dict[str, Any] = None, ttl: Optional[int] = None) -> bool:
    """Set cached content by type"""
    cache_key = get_cache_key(f"content:{content_type}", **filters or {})
    return cache_manager.set(cache_key, content, ttl)

async def invalidate_content_cache(content_type: str):
    """Invalidate all cached content for a specific type"""
    pattern = f"content:{content_type}:*"
    return cache_manager.clear_pattern(pattern)

# Cache TTL configurations
CACHE_TTL_CONFIG = {
    "hero_content": 3600,        # 1 hour
    "site_settings": 7200,       # 2 hours
    "navigation": 7200,          # 2 hours
    "footer_sections": 7200,     # 2 hours
    "features": 1800,            # 30 minutes
    "testimonials": 1800,        # 30 minutes
    "process_steps": 1800,       # 30 minutes
    "specifications": 1800,      # 30 minutes
    "newsletter_signups": 300,   # 5 minutes
    "contact_forms": 300,        # 5 minutes
    "page_views": 60,            # 1 minute
    "search_results": 600        # 10 minutes
}

def get_cache_ttl(content_type: str) -> int:
    """Get cache TTL for content type"""
    return CACHE_TTL_CONFIG.get(content_type, 3600)  # Default 1 hour