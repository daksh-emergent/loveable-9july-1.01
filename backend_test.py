#!/usr/bin/env python3
"""
Backend API Testing Script
This script tests all the content API endpoints to ensure they are working correctly.
"""

import requests
import json
import sys
from typing import Dict, Any, List, Optional
import os

# Get the backend URL from the frontend .env file
BACKEND_URL = "https://3a82a61b-9a2e-4ae8-96c6-732a00056062.preview.emergentagent.com"
API_BASE_URL = f"{BACKEND_URL}/api"

def test_endpoint(endpoint: str, expected_status_code: int = 200) -> Dict[str, Any]:
    """Test an API endpoint and return the response"""
    url = f"{API_BASE_URL}{endpoint}"
    print(f"\nTesting endpoint: {url}")
    
    try:
        response = requests.get(url)
        status_code = response.status_code
        
        print(f"Status Code: {status_code}")
        if status_code != expected_status_code:
            print(f"❌ Expected status code {expected_status_code}, got {status_code}")
            return {"success": False, "status_code": status_code}
        
        try:
            data = response.json()
            print(f"Response structure: {json.dumps(data, indent=2)[:200]}...")
            
            # Check if response follows the ResponseModel structure
            if "success" not in data or "message" not in data:
                print("❌ Response does not follow ResponseModel structure")
                return {"success": False, "data": data}
            
            return {"success": True, "data": data}
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return {"success": False, "error": "Invalid JSON"}
    
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

def test_hero_content():
    """Test the hero content endpoint"""
    print("\n=== Testing Hero Content API ===")
    response = test_endpoint("/content/hero")
    
    if not response["success"]:
        return False
    
    expected_fields = ["title", "subtitle", "description", "cta_text", "cta_link", "background_image"]
    return validate_response_data(response["data"], expected_fields)

def test_features():
    """Test the features endpoint"""
    print("\n=== Testing Features API ===")
    response = test_endpoint("/content/features")
    
    if not response["success"]:
        return False
    
    # Check if we have all 6 features
    features = response["data"].get("data", [])
    if len(features) != 6:
        print(f"❌ Expected 6 features, got {len(features)}")
        return False
    
    print(f"✅ Found {len(features)} features as expected")
    
    expected_fields = ["title", "description", "icon_svg", "category"]
    return validate_response_data(response["data"], expected_fields)

def test_testimonials():
    """Test the testimonials endpoint"""
    print("\n=== Testing Testimonials API ===")
    response = test_endpoint("/content/testimonials")
    
    if not response["success"]:
        return False
    
    # Check if we have all 4 testimonials
    testimonials = response["data"].get("data", [])
    if len(testimonials) != 4:
        print(f"❌ Expected 4 testimonials, got {len(testimonials)}")
        return False
    
    print(f"✅ Found {len(testimonials)} testimonials as expected")
    
    expected_fields = ["content", "author", "role", "company", "gradient", "background_image"]
    return validate_response_data(response["data"], expected_fields)

def test_process_steps():
    """Test the process steps endpoint"""
    print("\n=== Testing Process Steps API ===")
    response = test_endpoint("/content/process-steps")
    
    if not response["success"]:
        return False
    
    # Check if we have all 4 process steps
    steps = response["data"].get("data", [])
    if len(steps) != 4:
        print(f"❌ Expected 4 process steps, got {len(steps)}")
        return False
    
    print(f"✅ Found {len(steps)} process steps as expected")
    
    expected_fields = ["number", "title", "description", "image_url", "step_type"]
    return validate_response_data(response["data"], expected_fields)

def test_specifications():
    """Test the specifications endpoint"""
    print("\n=== Testing Specifications API ===")
    response = test_endpoint("/content/specifications")
    
    if not response["success"]:
        return False
    
    expected_fields = ["section_title", "section_subtitle", "content", "section_number"]
    return validate_response_data(response["data"], expected_fields)

def test_navigation():
    """Test the navigation endpoint"""
    print("\n=== Testing Navigation API ===")
    response = test_endpoint("/content/navigation")
    
    if not response["success"]:
        return False
    
    expected_fields = ["label", "href", "target", "nav_type"]
    return validate_response_data(response["data"], expected_fields)

def test_footer():
    """Test the footer endpoint"""
    print("\n=== Testing Footer API ===")
    response = test_endpoint("/content/footer")
    
    if not response["success"]:
        return False
    
    expected_fields = ["title", "content", "section_type", "links"]
    return validate_response_data(response["data"], expected_fields)

def test_site_settings():
    """Test the site settings endpoint"""
    print("\n=== Testing Site Settings API ===")
    response = test_endpoint("/content/site-settings")
    
    if not response["success"]:
        return False
    
    expected_fields = ["site_title", "site_description", "logo_url", "favicon_url", "primary_color", "secondary_color"]
    return validate_response_data(response["data"], expected_fields)

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
        ("Site Settings", test_site_settings)
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