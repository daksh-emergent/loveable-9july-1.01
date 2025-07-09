#!/usr/bin/env python3
"""
Seed script to populate the database with initial content
This script extracts hardcoded content from the frontend and seeds the database
"""

import asyncio
import os
import sys
from pathlib import Path

# Add backend directory to path
sys.path.append(str(Path(__file__).parent))

from database import db_manager, create_document
from models import *

async def seed_hero_content():
    """Seed hero section content"""
    print("Seeding hero content...")
    
    hero_data = {
        "title": "Atlas: Where Code Meets Motion",
        "subtitle": "Purpose",
        "description": "The humanoid companion that learns and adapts alongside you.",
        "cta_text": "Request Access",
        "cta_link": "#get-access",
        "background_image": "/Header-background.webp",
        "lottie_animation_url": "/loop-header.lottie",
        "hero_image": "/lovable-uploads/5663820f-6c97-4492-9210-9eaa1a8dc415.png",
        "order": 1
    }
    
    hero_obj = HeroContent(**hero_data)
    await create_document("hero_content", hero_obj.dict())
    print("✓ Hero content seeded")

async def seed_features():
    """Seed features data"""
    print("Seeding features...")
    
    features_data = [
        {
            "title": "Adaptive Learning",
            "description": "Atlas learns from your interactions, continuously improving its responses and actions to better serve your needs.",
            "icon_svg": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 2a10 10 0 1 0 10 10 4 4 0 1 1-4-4"></path><path d="M12 8a4 4 0 1 0 4 4"></path><circle cx="12" cy="12" r="1"></circle></svg>',
            "category": "intelligence",
            "order": 1
        },
        {
            "title": "Natural Interaction",
            "description": "Communicate using natural language and gestures. Atlas understands context and responds appropriately.",
            "icon_svg": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path><polyline points="14 2 14 8 20 8"></polyline><path d="M9 13v-1h6v1"></path><path d="M11 18.5l-.5-1 1-.5.5 1.5-1 .5-.5-1 1-.5"></path><path d="M9.5 12 9 11H4"></path></svg>',
            "category": "interaction",
            "order": 2
        },
        {
            "title": "Precise Movement",
            "description": "Advanced motorized joints provide fluid, human-like movement with exceptional balance and coordination.",
            "icon_svg": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="18" height="11" x="3" y="11" rx="2"></rect><circle cx="12" cy="5" r="2"></circle><path d="M12 7v4"></path><line x1="8" x2="8" y1="16" y2="16"></line><line x1="16" x2="16" y1="16" y2="16"></line></svg>',
            "category": "movement",
            "order": 3
        },
        {
            "title": "Spatial Awareness",
            "description": "Advanced sensors and mapping technology allow Atlas to navigate complex environments with ease.",
            "icon_svg": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="7.5 4.21 12 6.81 16.5 4.21"></polyline><polyline points="7.5 19.79 7.5 14.6 3 12"></polyline><polyline points="21 12 16.5 14.6 16.5 19.79"></polyline><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" x2="12" y1="22.08" y2="12"></line></svg>',
            "category": "sensors",
            "order": 4
        },
        {
            "title": "Enhanced Security",
            "description": "Built-in protocols protect your data and privacy, while physical safeguards ensure safe operation.",
            "icon_svg": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"></path><path d="m14.5 9-5 5"></path><path d="m9.5 9 5 5"></path></svg>',
            "category": "security",
            "order": 5
        },
        {
            "title": "Task Assistance",
            "description": "From simple reminders to complex multi-step tasks, Atlas can assist with a wide range of activities.",
            "icon_svg": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M16 6H3v11a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1V9a1 1 0 0 0-1-1h-2"></path><path d="M8 6V4a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2"></path><line x1="12" x2="12" y1="11" y2="15"></line><line x1="10" x2="14" y1="13" y2="13"></line></svg>',
            "category": "assistance",
            "order": 6
        }
    ]
    
    for feature_data in features_data:
        feature_obj = Feature(**feature_data)
        await create_document("features", feature_obj.dict())
    
    print(f"✓ {len(features_data)} features seeded")

async def seed_testimonials():
    """Seed testimonials data"""
    print("Seeding testimonials...")
    
    testimonials_data = [
        {
            "content": "Atlas transformed our production line, handling repetitive tasks while our team focuses on innovation. 30% increase in output within three months.",
            "author": "Sarah Chen",
            "role": "VP of Operations",
            "company": "Axion Manufacturing",
            "gradient": "from-blue-700 via-indigo-800 to-purple-900",
            "background_image": "/background-section1.png",
            "rating": 5,
            "order": 1
        },
        {
            "content": "Implementing Atlas in our fulfillment centers reduced workplace injuries by 40% while improving order accuracy. The learning capabilities are remarkable.",
            "author": "Michael Rodriguez",
            "role": "Director of Logistics",
            "company": "GlobalShip",
            "gradient": "from-indigo-900 via-purple-800 to-orange-500",
            "background_image": "/background-section2.png",
            "rating": 5,
            "order": 2
        },
        {
            "content": "Atlas adapted to our lab protocols faster than any system we've used. It's like having another researcher who never gets tired and maintains perfect precision.",
            "author": "Dr. Amara Patel",
            "role": "Lead Scientist",
            "company": "BioAdvance Research",
            "gradient": "from-purple-800 via-pink-700 to-red-500",
            "background_image": "/background-section3.png",
            "rating": 5,
            "order": 3
        },
        {
            "content": "As a mid-size business, we never thought advanced robotics would be accessible to us. Atlas changed that equation entirely with its versatility and ease of deployment.",
            "author": "Jason Lee",
            "role": "CEO",
            "company": "Innovative Solutions Inc.",
            "gradient": "from-orange-600 via-red-500 to-purple-600",
            "background_image": "/background-section1.png",
            "rating": 5,
            "order": 4
        }
    ]
    
    for testimonial_data in testimonials_data:
        testimonial_obj = Testimonial(**testimonial_data)
        await create_document("testimonials", testimonial_obj.dict())
    
    print(f"✓ {len(testimonials_data)} testimonials seeded")

async def seed_process_steps():
    """Seed process/how-it-works steps"""
    print("Seeding process steps...")
    
    steps_data = [
        {
            "number": "01",
            "title": "Request Access",
            "description": "Fill out the application form to join our early access program and secure your spot in line.",
            "image_url": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?auto=format&fit=crop&w=800&q=80",
            "step_type": "process",
            "order": 1
        },
        {
            "number": "02",
            "title": "Personalization",
            "description": "We'll work with you to customize Atlas to your specific needs and preferences.",
            "image_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=800&q=80",
            "step_type": "process",
            "order": 2
        },
        {
            "number": "03",
            "title": "Integration",
            "description": "Atlas arrives at your location and is integrated into your living or working environment.",
            "image_url": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?auto=format&fit=crop&w=800&q=80",
            "step_type": "process",
            "order": 3
        },
        {
            "number": "04",
            "title": "Adaptation",
            "description": "Through daily interaction, Atlas learns and adapts to your routines, preferences, and needs.",
            "image_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=800&q=80",
            "step_type": "process",
            "order": 4
        }
    ]
    
    for step_data in steps_data:
        step_obj = ProcessStep(**step_data)
        await create_document("process_steps", step_obj.dict())
    
    print(f"✓ {len(steps_data)} process steps seeded")

async def seed_specifications():
    """Seed specifications data"""
    print("Seeding specifications...")
    
    specs_data = [
        {
            "section_title": "Specs",
            "section_subtitle": "Technical Specifications",
            "content": "Atlas works with your team, not instead of it. By handling repetitive tasks, improving safety conditions, and learning from every interaction, Atlas helps humans focus on what they do best: create, solve, and innovate.",
            "section_number": "3",
            "background_image": "/text-mask-image.jpg",
            "order": 1
        }
    ]
    
    for spec_data in specs_data:
        spec_obj = Specification(**spec_data)
        await create_document("specifications", spec_obj.dict())
    
    print(f"✓ {len(specs_data)} specifications seeded")

async def seed_navigation():
    """Seed navigation data"""
    print("Seeding navigation...")
    
    nav_data = [
        {
            "label": "Home",
            "href": "#",
            "target": "_self",
            "nav_type": "main",
            "order": 1
        },
        {
            "label": "About",
            "href": "#features",
            "target": "_self",
            "nav_type": "main",
            "order": 2
        },
        {
            "label": "Contact",
            "href": "#details",
            "target": "_self",
            "nav_type": "main",
            "order": 3
        }
    ]
    
    for nav_item in nav_data:
        nav_obj = NavigationItem(**nav_item)
        await create_document("navigation", nav_obj.dict())
    
    print(f"✓ {len(nav_data)} navigation items seeded")

async def seed_footer_sections():
    """Seed footer sections"""
    print("Seeding footer sections...")
    
    footer_data = [
        {
            "title": "About Atlas",
            "content": "The humanoid companion that learns and adapts alongside you.",
            "section_type": "about",
            "links": [],
            "order": 1
        },
        {
            "title": "Contact",
            "content": "Get in touch with us for more information.",
            "section_type": "contact",
            "links": [
                {"text": "Email", "url": "mailto:info@atlas-robot.com"},
                {"text": "Phone", "url": "tel:+1234567890"}
            ],
            "order": 2
        },
        {
            "title": "Social",
            "content": "Follow us on social media.",
            "section_type": "social",
            "links": [
                {"text": "Twitter", "url": "https://twitter.com/atlas-robot"},
                {"text": "LinkedIn", "url": "https://linkedin.com/company/atlas-robot"}
            ],
            "order": 3
        }
    ]
    
    for footer_item in footer_data:
        footer_obj = FooterSection(**footer_item)
        await create_document("footer_sections", footer_obj.dict())
    
    print(f"✓ {len(footer_data)} footer sections seeded")

async def seed_site_settings():
    """Seed site settings"""
    print("Seeding site settings...")
    
    settings_data = {
        "site_title": "Atlas Robot - Where Code Meets Motion",
        "site_description": "The humanoid companion that learns and adapts alongside you.",
        "logo_url": "/logo.svg",
        "favicon_url": "/favicon.ico",
        "primary_color": "#FE5C02",
        "secondary_color": "#6366F1",
        "contact_email": "info@atlas-robot.com",
        "contact_phone": "+1234567890",
        "social_links": {
            "twitter": "https://twitter.com/atlas-robot",
            "linkedin": "https://linkedin.com/company/atlas-robot",
            "github": "https://github.com/atlas-robot"
        },
        "seo_keywords": ["humanoid robot", "AI companion", "robotics", "automation", "artificial intelligence"],
        "order": 1
    }
    
    settings_obj = SiteSettings(**settings_data)
    await create_document("site_settings", settings_obj.dict())
    print("✓ Site settings seeded")

async def main():
    """Main function to run all seeding functions"""
    try:
        print("Starting database seeding...")
        
        # Connect to database
        await db_manager.connect()
        
        # Create indexes
        await db_manager.create_indexes()
        
        # Seed all data
        await seed_hero_content()
        await seed_features()
        await seed_testimonials()
        await seed_process_steps()
        await seed_specifications()
        await seed_navigation()
        await seed_footer_sections()
        await seed_site_settings()
        
        print("\n✅ Database seeding completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        raise
    finally:
        await db_manager.disconnect()

if __name__ == "__main__":
    asyncio.run(main())