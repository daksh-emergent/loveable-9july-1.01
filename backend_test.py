#!/usr/bin/env python3
"""
Backend API Testing Script
This script tests all the content API endpoints to ensure they are working correctly,
with a focus on caching and database query optimization.
"""

import requests
import json
import sys
import time
from typing import Dict, Any, List, Optional
import os

# Get the backend URL from the frontend .env file
BACKEND_URL = "https://3a82a61b-9a2e-4ae8-96c6-732a00056062.preview.emergentagent.com"
API_BASE_URL = f"{BACKEND_URL}/api"

def test_endpoint(endpoint: str, expected_status_code: int = 200, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Test an API endpoint and return the response with timing information"""
    url = f"{API_BASE_URL}{endpoint}"
    print(f"\nTesting endpoint: {url}")
    if params:
        print(f"With parameters: {params}")
    
    try:
        start_time = time.time()
        response = requests.get(url, params=params)
        end_time = time.time()
        response_time = end_time - start_time
        
        status_code = response.status_code
        
        print(f"Status Code: {status_code}")
        print(f"Response Time: {response_time:.4f} seconds")
        
        if status_code != expected_status_code:
            print(f"❌ Expected status code {expected_status_code}, got {status_code}")
            return {"success": False, "status_code": status_code, "response_time": response_time}
        
        try:
            data = response.json()
            print(f"Response structure: {json.dumps(data, indent=2)[:200]}...")
            
            # Check if response follows the ResponseModel structure
            if "success" not in data or "message" not in data:
                print("❌ Response does not follow ResponseModel structure")
                return {"success": False, "data": data, "response_time": response_time}
            
            # Check if response indicates it came from cache
            is_cached = "from cache" in data.get("message", "").lower()
            if is_cached:
                print("✅ Response was served from cache")
            
            return {
                "success": True, 
                "data": data, 
                "response_time": response_time,
                "is_cached": is_cached
            }
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return {"success": False, "error": "Invalid JSON", "response_time": response_time}
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"success": False, "error": str(e)}

def validate_response_data(data: Dict[str, Any], expected_fields: List[str]) -> bool:
    """Validate that the response data contains the expected fields"""
    if not data.get("success", False):
        print(f"❌ Response indicates failure: {data.get('message', 'No message')}")
        return False
    
    response_data = data.get("data")
    if not response_data:
        print("❌ Response data is empty")
        return False
    
    # If response_data is a list, check the first item
    if isinstance(response_data, list):
        if not response_data:
            print("❌ Response data list is empty")
            return False
        item = response_data[0]
    else:
        item = response_data
    
    missing_fields = [field for field in expected_fields if field not in item]
    if missing_fields:
        print(f"❌ Missing fields in response: {missing_fields}")
        return False
    
    print("✅ Response data contains all expected fields")
    return True

def test_caching(endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Test if caching is working by making two consecutive requests"""
    print(f"\n=== Testing Caching for {endpoint} ===")
    
    # First request should not be cached
    first_response = test_endpoint(endpoint, params=params)
    if not first_response["success"]:
        print("❌ First request failed, cannot test caching")
        return {"success": False, "error": "First request failed"}
    
    # Second request should be cached
    second_response = test_endpoint(endpoint, params=params)
    if not second_response["success"]:
        print("❌ Second request failed, cannot test caching")
        return {"success": False, "error": "Second request failed"}
    
    # Check if second response was faster (indicating cache hit)
    first_time = first_response["response_time"]
    second_time = second_response["response_time"]
    time_improvement = (first_time - second_time) / first_time * 100
    
    print(f"First request: {first_time:.4f} seconds")
    print(f"Second request: {second_time:.4f} seconds")
    print(f"Time improvement: {time_improvement:.2f}%")
    
    # Check if second response indicates it came from cache
    is_cached = second_response.get("is_cached", False)
    
    if is_cached or (time_improvement > 20):  # If 20% faster, likely cached
        print("✅ Caching is working correctly")
        return {
            "success": True, 
            "time_improvement": time_improvement,
            "is_cached": is_cached
        }
    else:
        print("❌ Caching does not appear to be working")
        return {
            "success": False, 
            "time_improvement": time_improvement,
            "is_cached": is_cached
        }

def test_hero_content():
    """Test the hero content endpoint with caching"""
    print("\n=== Testing Hero Content API ===")
    
    # Test basic functionality
    response = test_endpoint("/content/hero")
    if not response["success"]:
        return False
    
    expected_fields = ["title", "subtitle", "description", "cta_text", "cta_link", "background_image"]
    data_valid = validate_response_data(response["data"], expected_fields)
    
    # Test caching
    cache_test = test_caching("/content/hero")
    
    return data_valid and cache_test["success"]

def test_features():
    """Test the features endpoint with filtering and caching"""
    print("\n=== Testing Features API ===")
    
    # Test basic functionality
    response = test_endpoint("/content/features")
    if not response["success"]:
        return False
    
    # Check if we have features
    features = response["data"].get("data", [])
    if not features:
        print(f"❌ No features found")
        return False
    
    print(f"✅ Found {len(features)} features")
    
    # Test with category filter to test compound indexes
    if len(features) > 0:
        # Get a category from the first feature
        category = features[0].get("category", "general")
        print(f"\n=== Testing Features API with category filter: {category} ===")
        
        filtered_response = test_endpoint("/content/features", params={"category": category})
        if not filtered_response["success"]:
            print("❌ Filtered request failed")
            return False
        
        filtered_features = filtered_response["data"].get("data", [])
        if not filtered_features:
            print(f"❌ No features found with category: {category}")
            return False
        
        print(f"✅ Found {len(filtered_features)} features with category: {category}")
        
        # Verify all returned features have the correct category
        all_match = all(feature.get("category") == category for feature in filtered_features)
        if not all_match:
            print("❌ Some features have incorrect category")
            return False
        
        print("✅ All filtered features have correct category")
        
        # Test caching with filtered request
        cache_test = test_caching("/content/features", params={"category": category})
    else:
        # Test caching with unfiltered request
        cache_test = test_caching("/content/features")
    
    expected_fields = ["title", "description", "icon_svg", "category"]
    data_valid = validate_response_data(response["data"], expected_fields)
    
    return data_valid and cache_test["success"]

def test_testimonials():
    """Test the testimonials endpoint with limit parameter and caching"""
    print("\n=== Testing Testimonials API ===")
    
    # Test basic functionality
    response = test_endpoint("/content/testimonials")
    if not response["success"]:
        return False
    
    # Test with limit parameter
    limit = 2
    print(f"\n=== Testing Testimonials API with limit: {limit} ===")
    
    limited_response = test_endpoint("/content/testimonials", params={"limit": limit})
    if not limited_response["success"]:
        print("❌ Limited request failed")
        return False
    
    limited_testimonials = limited_response["data"].get("data", [])
    if len(limited_testimonials) > limit:
        print(f"❌ Expected at most {limit} testimonials, got {len(limited_testimonials)}")
        return False
    
    print(f"✅ Received {len(limited_testimonials)} testimonials with limit {limit}")
    
    # Test caching with limited request
    cache_test = test_caching("/content/testimonials", params={"limit": limit})
    
    expected_fields = ["content", "author", "role", "company", "gradient", "background_image"]
    data_valid = validate_response_data(response["data"], expected_fields)
    
    return data_valid and cache_test["success"]

def test_process_steps():
    """Test the process steps endpoint with caching"""
    print("\n=== Testing Process Steps API ===")
    
    # Test basic functionality
    response = test_endpoint("/content/process-steps")
    if not response["success"]:
        return False
    
    # Test with step_type parameter
    step_type = "process"
    print(f"\n=== Testing Process Steps API with step_type: {step_type} ===")
    
    filtered_response = test_endpoint("/content/process-steps", params={"step_type": step_type})
    if not filtered_response["success"]:
        print("❌ Filtered request failed")
        return False
    
    # Test caching
    cache_test = test_caching("/content/process-steps")
    
    expected_fields = ["number", "title", "description", "image_url", "step_type"]
    data_valid = validate_response_data(response["data"], expected_fields)
    
    return data_valid and cache_test["success"]

def test_specifications():
    """Test the specifications endpoint with caching"""
    print("\n=== Testing Specifications API ===")
    
    # Test basic functionality
    response = test_endpoint("/content/specifications")
    if not response["success"]:
        return False
    
    # Test caching
    cache_test = test_caching("/content/specifications")
    
    expected_fields = ["section_title", "section_subtitle", "content", "section_number"]
    data_valid = validate_response_data(response["data"], expected_fields)
    
    return data_valid and cache_test["success"]

def test_navigation():
    """Test the navigation endpoint with nav_type parameter and caching"""
    print("\n=== Testing Navigation API ===")
    
    # Test basic functionality
    response = test_endpoint("/content/navigation")
    if not response["success"]:
        return False
    
    # Test with nav_type parameter
    nav_type = "main"
    print(f"\n=== Testing Navigation API with nav_type: {nav_type} ===")
    
    filtered_response = test_endpoint("/content/navigation", params={"nav_type": nav_type})
    if not filtered_response["success"]:
        print("❌ Filtered request failed")
        return False
    
    # Test caching
    cache_test = test_caching("/content/navigation")
    
    expected_fields = ["label", "href", "target", "nav_type"]
    data_valid = validate_response_data(response["data"], expected_fields)
    
    return data_valid and cache_test["success"]

def test_footer():
    """Test the footer endpoint with caching"""
    print("\n=== Testing Footer API ===")
    
    # Test basic functionality
    response = test_endpoint("/content/footer")
    if not response["success"]:
        return False
    
    # Test caching
    cache_test = test_caching("/content/footer")
    
    expected_fields = ["title", "content", "section_type", "links"]
    data_valid = validate_response_data(response["data"], expected_fields)
    
    return data_valid and cache_test["success"]

def test_site_settings():
    """Test the site settings endpoint with caching"""
    print("\n=== Testing Site Settings API ===")
    
    # Test basic functionality
    response = test_endpoint("/content/site-settings")
    if not response["success"]:
        return False
    
    # Test caching
    cache_test = test_caching("/content/site-settings")
    
    expected_fields = ["site_title", "site_description", "logo_url", "favicon_url", "primary_color", "secondary_color"]
    data_valid = validate_response_data(response["data"], expected_fields)
    
    return data_valid and cache_test["success"]

def test_cache_invalidation():
    """Test cache invalidation by creating a new resource and checking if cache is updated"""
    print("\n=== Testing Cache Invalidation ===")
    
    # First, get the current hero content and cache it
    print("Step 1: Get current hero content and cache it")
    first_response = test_endpoint("/content/hero")
    if not first_response["success"]:
        print("❌ Could not get current hero content")
        return False
    
    # Make a second request to ensure it's cached
    print("Step 2: Make a second request to ensure it's cached")
    second_response = test_endpoint("/content/hero")
    if not second_response["success"]:
        print("❌ Second request failed")
        return False
    
    # Create a new hero content to invalidate cache
    print("Step 3: Create a new hero content to invalidate cache")
    new_hero = {
        "title": "New Hero Title",
        "subtitle": "New Hero Subtitle",
        "description": "This is a new hero description for testing cache invalidation",
        "cta_text": "Click Me Now",
        "cta_link": "/contact",
        "background_image": "/images/new-hero-bg.jpg"
    }
    
    try:
        create_response = requests.post(f"{API_BASE_URL}/content/hero", json=new_hero)
        if create_response.status_code != 200:
            print(f"❌ Failed to create new hero content: {create_response.status_code}")
            return False
        
        print("✅ Created new hero content")
        
        # Get the hero content again, should not be cached
        print("Step 4: Get the hero content again, should not be cached")
        third_response = test_endpoint("/content/hero")
        if not third_response["success"]:
            print("❌ Third request failed")
            return False
        
        # Check if the new hero content is returned
        hero_data = third_response["data"].get("data", {})
        if hero_data.get("title") != "New Hero Title":
            print("❌ Cache invalidation failed, old content still returned")
            return False
        
        print("✅ Cache invalidation successful, new content returned")
        return True
        
    except Exception as e:
        print(f"❌ Error testing cache invalidation: {e}")
        return False

def run_all_tests():
    """Run all API tests and report results"""
    print("Starting API tests...\n")
    
    # Test the base API endpoint
    base_response = test_endpoint("")
    if not base_response["success"]:
        print("❌ Base API endpoint test failed")
    else:
        print("✅ Base API endpoint test passed")
    
    # Run all content API tests
    tests = [
        ("Hero Content", test_hero_content),
        ("Features", test_features),
        ("Testimonials", test_testimonials),
        ("Process Steps", test_process_steps),
        ("Specifications", test_specifications),
        ("Navigation", test_navigation),
        ("Footer", test_footer),
        ("Site Settings", test_site_settings),
        ("Cache Invalidation", test_cache_invalidation)
    ]
    
    results = {}
    for name, test_func in tests:
        print(f"\n{'=' * 50}")
        print(f"Running test: {name}")
        result = test_func()
        results[name] = result
        print(f"{'=' * 50}")
    
    # Print summary
    print("\n\n=== TEST SUMMARY ===")
    all_passed = True
    for name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        if not result:
            all_passed = False
        print(f"{name}: {status}")
    
    if all_passed:
        print("\n🎉 All API tests passed successfully!")
        return 0
    else:
        print("\n❌ Some API tests failed. See details above.")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())