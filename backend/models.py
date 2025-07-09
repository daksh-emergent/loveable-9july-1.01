from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

# Base model for all content with common fields
class ContentBase(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True
    order: int = 0

# Hero Section Model
class HeroContent(ContentBase):
    title: str
    subtitle: str
    description: str
    cta_text: str
    cta_link: str
    background_image: str
    lottie_animation_url: Optional[str] = None
    hero_image: Optional[str] = None

class HeroContentCreate(BaseModel):
    title: str
    subtitle: str
    description: str
    cta_text: str
    cta_link: str
    background_image: str
    lottie_animation_url: Optional[str] = None
    hero_image: Optional[str] = None

# Features Model
class Feature(ContentBase):
    title: str
    description: str
    icon_svg: str
    category: str = "general"

class FeatureCreate(BaseModel):
    title: str
    description: str
    icon_svg: str
    category: str = "general"
    order: int = 0

# Testimonials Model
class Testimonial(ContentBase):
    content: str
    author: str
    role: str
    company: str
    gradient: str
    background_image: str
    rating: int = 5

class TestimonialCreate(BaseModel):
    content: str
    author: str
    role: str
    company: str
    gradient: str
    background_image: str
    rating: int = 5
    order: int = 0

# How It Works / Steps Model
class ProcessStep(ContentBase):
    number: str
    title: str
    description: str
    image_url: str
    step_type: str = "process"

class ProcessStepCreate(BaseModel):
    number: str
    title: str
    description: str
    image_url: str
    step_type: str = "process"
    order: int = 0

# Specifications Model
class Specification(ContentBase):
    section_title: str
    section_subtitle: str
    content: str
    section_number: str
    background_image: Optional[str] = None

class SpecificationCreate(BaseModel):
    section_title: str
    section_subtitle: str
    content: str
    section_number: str
    background_image: Optional[str] = None
    order: int = 0

# Navigation Model
class NavigationItem(ContentBase):
    label: str
    href: str
    target: str = "_self"
    nav_type: str = "main"  # main, footer, mobile
    parent_id: Optional[str] = None

class NavigationItemCreate(BaseModel):
    label: str
    href: str
    target: str = "_self"
    nav_type: str = "main"
    parent_id: Optional[str] = None
    order: int = 0

# Footer Model
class FooterSection(ContentBase):
    title: str
    content: str
    section_type: str  # about, contact, social, legal
    links: List[Dict[str, str]] = []

class FooterSectionCreate(BaseModel):
    title: str
    content: str
    section_type: str
    links: List[Dict[str, str]] = []
    order: int = 0

# Newsletter Model
class NewsletterSignup(ContentBase):
    email: str
    name: Optional[str] = None
    interests: List[str] = []
    source: str = "website"
    status: str = "subscribed"  # subscribed, unsubscribed, pending

class NewsletterSignupCreate(BaseModel):
    email: str
    name: Optional[str] = None
    interests: List[str] = []
    source: str = "website"

# Site Settings Model
class SiteSettings(ContentBase):
    site_title: str
    site_description: str
    logo_url: str
    favicon_url: str
    primary_color: str
    secondary_color: str
    contact_email: str
    contact_phone: Optional[str] = None
    social_links: Dict[str, str] = {}
    analytics_code: Optional[str] = None
    seo_keywords: List[str] = []

class SiteSettingsCreate(BaseModel):
    site_title: str
    site_description: str
    logo_url: str
    favicon_url: str
    primary_color: str
    secondary_color: str
    contact_email: str
    contact_phone: Optional[str] = None
    social_links: Dict[str, str] = {}
    analytics_code: Optional[str] = None
    seo_keywords: List[str] = []

# Content Management Model for CMS functionality
class ContentPage(ContentBase):
    title: str
    slug: str
    content: str
    meta_description: str
    meta_keywords: List[str] = []
    published: bool = True
    featured_image: Optional[str] = None
    page_type: str = "standard"  # standard, landing, blog, etc.

class ContentPageCreate(BaseModel):
    title: str
    slug: str
    content: str
    meta_description: str
    meta_keywords: List[str] = []
    published: bool = True
    featured_image: Optional[str] = None
    page_type: str = "standard"

# Analytics Model for tracking
class PageView(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    page_path: str
    referrer: Optional[str] = None
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    session_id: Optional[str] = None
    country: Optional[str] = None
    device_type: Optional[str] = None

class PageViewCreate(BaseModel):
    page_path: str
    referrer: Optional[str] = None
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None
    session_id: Optional[str] = None
    country: Optional[str] = None
    device_type: Optional[str] = None

# Contact Form Model
class ContactForm(ContentBase):
    name: str
    email: str
    subject: str
    message: str
    phone: Optional[str] = None
    company: Optional[str] = None
    status: str = "new"  # new, in_progress, resolved, closed

class ContactFormCreate(BaseModel):
    name: str
    email: str
    subject: str
    message: str
    phone: Optional[str] = None
    company: Optional[str] = None