from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import logging
from datetime import datetime

from models import (
    HeroContent, HeroContentCreate,
    Feature, FeatureCreate,
    Testimonial, TestimonialCreate,
    ProcessStep, ProcessStepCreate,
    Specification, SpecificationCreate,
    NavigationItem, NavigationItemCreate,
    FooterSection, FooterSectionCreate,
    NewsletterSignup, NewsletterSignupCreate,
    SiteSettings, SiteSettingsCreate,
    ContentPage, ContentPageCreate,
    PageView, PageViewCreate,
    ContactForm, ContactFormCreate
)

from database import (
    get_all_documents, get_document_by_id, create_document, 
    update_document, delete_document, search_documents
)

logger = logging.getLogger(__name__)
router = APIRouter()

# Response models
class ResponseModel(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None

class PaginatedResponse(BaseModel):
    success: bool
    message: str
    data: List[Any]
    total: int
    page: int
    per_page: int
    total_pages: int

# Hero Content Endpoints
@router.get("/hero", response_model=ResponseModel)
async def get_hero_content():
    """Get active hero content"""
    try:
        hero_data = await get_all_documents("hero_content", {"is_active": True}, limit=1)
        if not hero_data:
            return ResponseModel(success=False, message="No hero content found")
        
        return ResponseModel(
            success=True,
            message="Hero content retrieved successfully",
            data=hero_data[0]
        )
    except Exception as e:
        logger.error(f"Error getting hero content: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/hero", response_model=ResponseModel)
async def create_hero_content(hero_data: HeroContentCreate):
    """Create new hero content"""
    try:
        # Deactivate existing hero content
        existing_hero = await get_all_documents("hero_content", {"is_active": True})
        for hero in existing_hero:
            await update_document("hero_content", hero["id"], {"is_active": False})
        
        # Create new hero content
        hero_dict = hero_data.dict()
        hero_obj = HeroContent(**hero_dict)
        created_hero = await create_document("hero_content", hero_obj.dict())
        
        return ResponseModel(
            success=True,
            message="Hero content created successfully",
            data=created_hero
        )
    except Exception as e:
        logger.error(f"Error creating hero content: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Features Endpoints
@router.get("/features", response_model=ResponseModel)
async def get_features(category: Optional[str] = None):
    """Get all active features, optionally filtered by category"""
    try:
        filter_dict = {"is_active": True}
        if category:
            filter_dict["category"] = category
            
        features = await get_all_documents("features", filter_dict, "order", 1)
        
        return ResponseModel(
            success=True,
            message="Features retrieved successfully",
            data=features
        )
    except Exception as e:
        logger.error(f"Error getting features: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/features", response_model=ResponseModel)
async def create_feature(feature_data: FeatureCreate):
    """Create a new feature"""
    try:
        feature_dict = feature_data.dict()
        feature_obj = Feature(**feature_dict)
        created_feature = await create_document("features", feature_obj.dict())
        
        return ResponseModel(
            success=True,
            message="Feature created successfully",
            data=created_feature
        )
    except Exception as e:
        logger.error(f"Error creating feature: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/features/{feature_id}", response_model=ResponseModel)
async def update_feature(feature_id: str, feature_data: FeatureCreate):
    """Update a feature"""
    try:
        updated_feature = await update_document("features", feature_id, feature_data.dict())
        if not updated_feature:
            raise HTTPException(status_code=404, detail="Feature not found")
            
        return ResponseModel(
            success=True,
            message="Feature updated successfully",
            data=updated_feature
        )
    except Exception as e:
        logger.error(f"Error updating feature: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Testimonials Endpoints
@router.get("/testimonials", response_model=ResponseModel)
async def get_testimonials(limit: int = Query(10, ge=1, le=100)):
    """Get all active testimonials"""
    try:
        testimonials = await get_all_documents("testimonials", {"is_active": True}, "order", 1, limit)
        
        return ResponseModel(
            success=True,
            message="Testimonials retrieved successfully",
            data=testimonials
        )
    except Exception as e:
        logger.error(f"Error getting testimonials: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/testimonials", response_model=ResponseModel)
async def create_testimonial(testimonial_data: TestimonialCreate):
    """Create a new testimonial"""
    try:
        testimonial_dict = testimonial_data.dict()
        testimonial_obj = Testimonial(**testimonial_dict)
        created_testimonial = await create_document("testimonials", testimonial_obj.dict())
        
        return ResponseModel(
            success=True,
            message="Testimonial created successfully",
            data=created_testimonial
        )
    except Exception as e:
        logger.error(f"Error creating testimonial: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Process Steps Endpoints
@router.get("/process-steps", response_model=ResponseModel)
async def get_process_steps(step_type: Optional[str] = "process"):
    """Get all active process steps"""
    try:
        filter_dict = {"is_active": True}
        if step_type:
            filter_dict["step_type"] = step_type
            
        steps = await get_all_documents("process_steps", filter_dict, "order", 1)
        
        return ResponseModel(
            success=True,
            message="Process steps retrieved successfully",
            data=steps
        )
    except Exception as e:
        logger.error(f"Error getting process steps: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/process-steps", response_model=ResponseModel)
async def create_process_step(step_data: ProcessStepCreate):
    """Create a new process step"""
    try:
        step_dict = step_data.dict()
        step_obj = ProcessStep(**step_dict)
        created_step = await create_document("process_steps", step_obj.dict())
        
        return ResponseModel(
            success=True,
            message="Process step created successfully",
            data=created_step
        )
    except Exception as e:
        logger.error(f"Error creating process step: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Specifications Endpoints
@router.get("/specifications", response_model=ResponseModel)
async def get_specifications():
    """Get all active specifications"""
    try:
        specifications = await get_all_documents("specifications", {"is_active": True}, "order", 1)
        
        return ResponseModel(
            success=True,
            message="Specifications retrieved successfully",
            data=specifications
        )
    except Exception as e:
        logger.error(f"Error getting specifications: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/specifications", response_model=ResponseModel)
async def create_specification(spec_data: SpecificationCreate):
    """Create a new specification"""
    try:
        spec_dict = spec_data.dict()
        spec_obj = Specification(**spec_dict)
        created_spec = await create_document("specifications", spec_obj.dict())
        
        return ResponseModel(
            success=True,
            message="Specification created successfully",
            data=created_spec
        )
    except Exception as e:
        logger.error(f"Error creating specification: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Navigation Endpoints
@router.get("/navigation", response_model=ResponseModel)
async def get_navigation(nav_type: Optional[str] = "main"):
    """Get navigation items by type"""
    try:
        filter_dict = {"is_active": True}
        if nav_type:
            filter_dict["nav_type"] = nav_type
            
        navigation = await get_all_documents("navigation", filter_dict, "order", 1)
        
        return ResponseModel(
            success=True,
            message="Navigation retrieved successfully",
            data=navigation
        )
    except Exception as e:
        logger.error(f"Error getting navigation: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/navigation", response_model=ResponseModel)
async def create_navigation_item(nav_data: NavigationItemCreate):
    """Create a new navigation item"""
    try:
        nav_dict = nav_data.dict()
        nav_obj = NavigationItem(**nav_dict)
        created_nav = await create_document("navigation", nav_obj.dict())
        
        return ResponseModel(
            success=True,
            message="Navigation item created successfully",
            data=created_nav
        )
    except Exception as e:
        logger.error(f"Error creating navigation item: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Footer Endpoints
@router.get("/footer", response_model=ResponseModel)
async def get_footer_sections():
    """Get all active footer sections"""
    try:
        footer_sections = await get_all_documents("footer_sections", {"is_active": True}, "order", 1)
        
        return ResponseModel(
            success=True,
            message="Footer sections retrieved successfully",
            data=footer_sections
        )
    except Exception as e:
        logger.error(f"Error getting footer sections: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/footer", response_model=ResponseModel)
async def create_footer_section(footer_data: FooterSectionCreate):
    """Create a new footer section"""
    try:
        footer_dict = footer_data.dict()
        footer_obj = FooterSection(**footer_dict)
        created_footer = await create_document("footer_sections", footer_obj.dict())
        
        return ResponseModel(
            success=True,
            message="Footer section created successfully",
            data=created_footer
        )
    except Exception as e:
        logger.error(f"Error creating footer section: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Newsletter Endpoints
@router.post("/newsletter/signup", response_model=ResponseModel)
async def newsletter_signup(signup_data: NewsletterSignupCreate):
    """Subscribe to newsletter"""
    try:
        # Check if email already exists
        existing_signup = await get_all_documents("newsletter_signups", {"email": signup_data.email})
        if existing_signup:
            return ResponseModel(
                success=False,
                message="Email already subscribed to newsletter"
            )
        
        signup_dict = signup_data.dict()
        signup_obj = NewsletterSignup(**signup_dict)
        created_signup = await create_document("newsletter_signups", signup_obj.dict())
        
        return ResponseModel(
            success=True,
            message="Successfully subscribed to newsletter",
            data=created_signup
        )
    except Exception as e:
        logger.error(f"Error creating newsletter signup: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/newsletter/subscribers", response_model=ResponseModel)
async def get_newsletter_subscribers(status: Optional[str] = "subscribed"):
    """Get newsletter subscribers"""
    try:
        filter_dict = {}
        if status:
            filter_dict["status"] = status
            
        subscribers = await get_all_documents("newsletter_signups", filter_dict, "created_at", -1)
        
        return ResponseModel(
            success=True,
            message="Newsletter subscribers retrieved successfully",
            data=subscribers
        )
    except Exception as e:
        logger.error(f"Error getting newsletter subscribers: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Site Settings Endpoints
@router.get("/site-settings", response_model=ResponseModel)
async def get_site_settings():
    """Get active site settings"""
    try:
        settings = await get_all_documents("site_settings", {"is_active": True}, limit=1)
        if not settings:
            return ResponseModel(success=False, message="No site settings found")
        
        return ResponseModel(
            success=True,
            message="Site settings retrieved successfully",
            data=settings[0]
        )
    except Exception as e:
        logger.error(f"Error getting site settings: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/site-settings", response_model=ResponseModel)
async def create_site_settings(settings_data: SiteSettingsCreate):
    """Create new site settings"""
    try:
        # Deactivate existing settings
        existing_settings = await get_all_documents("site_settings", {"is_active": True})
        for settings in existing_settings:
            await update_document("site_settings", settings["id"], {"is_active": False})
        
        # Create new settings
        settings_dict = settings_data.dict()
        settings_obj = SiteSettings(**settings_dict)
        created_settings = await create_document("site_settings", settings_obj.dict())
        
        return ResponseModel(
            success=True,
            message="Site settings created successfully",
            data=created_settings
        )
    except Exception as e:
        logger.error(f"Error creating site settings: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Contact Form Endpoints
@router.post("/contact", response_model=ResponseModel)
async def submit_contact_form(contact_data: ContactFormCreate):
    """Submit contact form"""
    try:
        contact_dict = contact_data.dict()
        contact_obj = ContactForm(**contact_dict)
        created_contact = await create_document("contact_forms", contact_obj.dict())
        
        return ResponseModel(
            success=True,
            message="Contact form submitted successfully",
            data=created_contact
        )
    except Exception as e:
        logger.error(f"Error submitting contact form: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Analytics Endpoints
@router.post("/analytics/pageview", response_model=ResponseModel)
async def track_page_view(page_view_data: PageViewCreate):
    """Track page view for analytics"""
    try:
        page_view_dict = page_view_data.dict()
        page_view_obj = PageView(**page_view_dict)
        created_page_view = await create_document("page_views", page_view_obj.dict())
        
        return ResponseModel(
            success=True,
            message="Page view tracked successfully",
            data=created_page_view
        )
    except Exception as e:
        logger.error(f"Error tracking page view: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Search Endpoints
@router.get("/search", response_model=ResponseModel)
async def search_content(
    query: str = Query(..., min_length=1),
    content_type: Optional[str] = None
):
    """Search across all content types"""
    try:
        results = []
        
        # Search in features
        if not content_type or content_type == "features":
            feature_results = await search_documents("features", query, ["title", "description"])
            for result in feature_results:
                result["content_type"] = "feature"
                results.append(result)
        
        # Search in testimonials
        if not content_type or content_type == "testimonials":
            testimonial_results = await search_documents("testimonials", query, ["content", "author", "role"])
            for result in testimonial_results:
                result["content_type"] = "testimonial"
                results.append(result)
        
        # Search in process steps
        if not content_type or content_type == "process_steps":
            step_results = await search_documents("process_steps", query, ["title", "description"])
            for result in step_results:
                result["content_type"] = "process_step"
                results.append(result)
        
        # Search in specifications
        if not content_type or content_type == "specifications":
            spec_results = await search_documents("specifications", query, ["section_title", "content"])
            for result in spec_results:
                result["content_type"] = "specification"
                results.append(result)
        
        # Sort results by relevance (this could be enhanced with better scoring)
        results.sort(key=lambda x: x.get("order", 0))
        
        return ResponseModel(
            success=True,
            message=f"Search completed. Found {len(results)} results",
            data=results
        )
    except Exception as e:
        logger.error(f"Error searching content: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")