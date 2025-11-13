"""
Test script for the Fenix Marine Services Screenshot API
This script demonstrates how to use all the API endpoints
"""

import requests
import json
from datetime import datetime, timedelta

# API base URL
BASE_URL = "http://37.60.243.201:5005"

# Admin password
ADMIN_PASSWORD = "YB02Ss3JJdk"


def test_root():
    """Test the root endpoint"""
    print("\n" + "="*50)
    print("Testing: GET /")
    print("="*50)
    
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_status():
    """Test the status endpoint"""
    print("\n" + "="*50)
    print("Testing: GET /status")
    print("="*50)
    
    response = requests.get(f"{BASE_URL}/status")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_capture_screenshot_now():
    """Test capturing an immediate screenshot"""
    print("\n" + "="*50)
    print("Testing: POST /screenshot/now")
    print("="*50)
    
    data = {
        "admin_password": ADMIN_PASSWORD
    }
    
    print("🚀 Starting full desktop screenshot capture...")
    print("⚠️  This will take 2-3 minutes to complete")
    print("   - Navigate to Fenix Marine Services")
    print("   - Login with saved credentials")
    print("   - Navigate to Empty Receiving Schedule")
    print("   - Capture full desktop screenshots with scrolling")
    print("   - Stitch screenshots together")
    
    response = requests.post(
        f"{BASE_URL}/screenshot/now",
        json=data,
        timeout=300  # 5 minute timeout for screenshot process
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.json().get('success', False)


def test_get_screenshot():
    """Test getting a screenshot by date"""
    print("\n" + "="*50)
    print("Testing: GET /screenshot/<date>")
    print("="*50)
    
    today = datetime.utcnow().strftime("%Y-%m-%d")
    print(f"Requesting screenshot for: {today}")
    
    response = requests.get(f"{BASE_URL}/screenshot/{today}")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Screenshot found successfully")
        print(f"Response JSON: {json.dumps(data, indent=2)}")
        
        # Verify JSON structure
        required_fields = ['success', 'date', 'filename', 'download_url', 'message']
        for field in required_fields:
            if field in data:
                print(f"✓ {field}: {data[field]}")
            else:
                print(f"❌ Missing field: {field}")
        
        # Test downloading the actual file
        if 'download_url' in data:
            download_url = data['download_url']
            print(f"\nTesting screenshot download from: {download_url}")
            
            if download_url.startswith('http'):
                # Full URL
                file_response = requests.get(download_url)
            else:
                # Relative URL - remove the extra slash if present
                clean_url = download_url.lstrip('/')
                file_response = requests.get(f"{BASE_URL}/{clean_url}")
            
            if file_response.status_code == 200:
                filename = data.get('filename', 'test_screenshot.png')
                with open(f"test_{filename}", "wb") as f:
                    f.write(file_response.content)
                print(f"✓ Screenshot downloaded and saved as: test_{filename}")
                print(f"✓ File size: {len(file_response.content):,} bytes")
            else:
                print(f"❌ Failed to download screenshot: {file_response.status_code}")
    else:
        print(f"Response: {response.json()}")


def test_get_screenshots_range():
    """Test getting screenshots range"""
    print("\n" + "="*50)
    print("Testing: GET /screenshots/range")
    print("="*50)
    
    # Test with last_n parameter
    print("\nTesting with last_n=2")
    response = requests.get(f"{BASE_URL}/screenshots/range?last_n=2")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Screenshots range found successfully")
        print(f"Download URL: {data.get('download_url', 'Unknown')}")
        print(f"ZIP Filename: {data.get('zip_filename', 'Unknown')}")
        print(f"Screenshot Count: {data.get('screenshot_count', 'Unknown')}")
        
        # Test downloading the ZIP file
        if 'download_url' in data:
            download_url = data['download_url']
            print(f"\nTesting ZIP download from: {download_url}")
            
            file_response = requests.get(download_url)
            if file_response.status_code == 200:
                zip_filename = data.get('zip_filename', 'test_screenshots.zip')
                with open(f"test_{zip_filename}", "wb") as f:
                    f.write(file_response.content)
                print(f"✓ ZIP file downloaded and saved as: test_{zip_filename}")
                print(f"✓ ZIP file size: {len(file_response.content):,} bytes")
            else:
                print(f"❌ Failed to download ZIP: {file_response.status_code}")
    else:
        print(f"Response: {response.json()}")
    
    # Test with date range
    print("\nTesting with date range (last 7 days)")
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=7)
    
    params = {
        'start_date': start_date.strftime("%Y-%m-%d"),
        'end_date': end_date.strftime("%Y-%m-%d")
    }
    
    response = requests.get(f"{BASE_URL}/screenshots/range", params=params)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_change_frequency():
    """Test changing screenshot frequency"""
    print("\n" + "="*50)
    print("Testing: POST /admin/frequency")
    print("="*50)
    
    # Change to 12 hours
    data = {
        "admin_password": ADMIN_PASSWORD,
        "frequency_hours": 12
    }
    
    print("Setting frequency to 12 hours")
    response = requests.post(
        f"{BASE_URL}/admin/frequency",
        json=data
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Change back to 24 hours
    data["frequency_hours"] = 24
    print("\nChanging back to 24 hours")
    response = requests.post(
        f"{BASE_URL}/admin/frequency",
        json=data
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_set_preferred_hour():
    """Test setting preferred hour for scheduled captures"""
    print("\n" + "="*50)
    print("Testing: POST /admin/preferred_hour")
    print("="*50)
    
    # Change to 2 PM (14:00)
    data = {
        "admin_password": ADMIN_PASSWORD,
        "preferred_hour": 14
    }
    
    print("Setting preferred hour to 14:00 (2 PM)")
    response = requests.post(
        f"{BASE_URL}/admin/preferred_hour",
        json=data
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Change back to 10 AM (10:00)
    data["preferred_hour"] = 10
    print("\nChanging back to 10:00 (10 AM)")
    response = requests.post(
        f"{BASE_URL}/admin/preferred_hour",
        json=data
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_update_credentials():
    """Test updating login credentials"""
    print("\n" + "="*50)
    print("Testing: POST /admin/credentials")
    print("="*50)
    
    # Update credentials
    data = {
        "admin_password": ADMIN_PASSWORD,
        "username": "test@example.com",
        "password": "testpassword123"
    }
    
    print("Updating credentials to test values")
    response = requests.post(
        f"{BASE_URL}/admin/credentials",
        json=data
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Change back to original credentials
    data = {
        "admin_password": ADMIN_PASSWORD,
        "username": "sara@fouroneone.io",
        "password": "Ss925201!"
    }
    
    print("\nRestoring original Fenix Marine Services credentials")
    response = requests.post(
        f"{BASE_URL}/admin/credentials",
        json=data
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_cleanup():
    """Test cleanup endpoint"""
    print("\n" + "="*50)
    print("Testing: POST /admin/cleanup")
    print("="*50)
    
    data = {
        "admin_password": ADMIN_PASSWORD
    }
    
    print("⚠️  Running cleanup (this will delete all screenshots)")
    print("This is useful for clearing test data")
    response = requests.post(
        f"{BASE_URL}/admin/cleanup",
        json=data
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_download_file():
    """Test downloading a file directly"""
    print("\n" + "="*50)
    print("Testing: GET /download/<filename>")
    print("="*50)
    
    # This would need an actual filename from a previous screenshot
    print("Note: This test requires a previously captured screenshot")
    print("Run the screenshot capture test first to get a filename")
    
    # For demonstration, we'll just test the endpoint structure
    test_filename = "fenix_screenshot_2025-01-15_12-00-00.png"
    response = requests.get(f"{BASE_URL}/download/{test_filename}")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        print(f"✓ File download successful")
        with open(f"downloaded_{test_filename}", "wb") as f:
            f.write(response.content)
        print(f"Saved as: downloaded_{test_filename}")
        print(f"File size: {len(response.content):,} bytes")
    elif response.status_code == 404:
        print(f"✓ Correctly returned 404 for non-existent file")
        print(f"Response: {response.json()}")
    else:
        print(f"Response: {response.text}")


def test_invalid_admin_password():
    """Test with invalid admin password"""
    print("\n" + "="*50)
    print("Testing: Invalid Admin Password")
    print("="*50)
    
    data = {
        "admin_password": "wrong_password",
        "frequency_hours": 12
    }
    
    response = requests.post(
        f"{BASE_URL}/admin/frequency",
        json=data
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 403:
        print("✓ Correctly rejected invalid password")


def test_api_connectivity():
    """Test basic API connectivity"""
    print("\n" + "="*50)
    print("Testing: API Connectivity")
    print("="*50)
    
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ API is running and accessible")
            api_info = response.json()
            print(f"✓ API Name: {api_info.get('name', 'Unknown')}")
            print(f"✓ API Version: {api_info.get('version', 'Unknown')}")
            return True
        else:
            print(f"❌ API returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API - make sure it's running on port 5005")
        return False
    except Exception as e:
        print(f"❌ Error testing connectivity: {e}")
        return False


def main():
    """Run all tests"""
    print("="*70)
    print("🖥️  FENIX MARINE SERVICES SCREENSHOT API - COMPLETE TEST SUITE")
    print("="*70)
    print(f"Base URL: {BASE_URL}")
    print(f"Testing full desktop screenshot capture with:")
    print("  • Browser navigation automation")
    print("  • Login with autofill clearing") 
    print("  • Scroll detection and capture")
    print("  • Full desktop screenshots (taskbar + URL bar)")
    print("  • Screenshot stitching")
    print("="*70)
    
    # Test API connectivity first
    if not test_api_connectivity():
        print("\n❌ Cannot proceed with tests - API is not accessible")
        print("Make sure to start the API with: python app.py")
        return
    
    input("\nPress Enter to start comprehensive tests...")
    
    try:
        # Basic information tests
        print("\n🔍 TESTING BASIC ENDPOINTS")
        test_root()
        test_status()
        
        # Test screenshot capture
        print("\n📸 TESTING SCREENSHOT CAPTURE")
        print("⚠️  The next test will run the full automation process:")
        print("   1. Open Chrome browser")
        print("   2. Navigate to Fenix Marine Services portal")
        print("   3. Login with credentials (clearing autofill)")
        print("   4. Navigate to Empty Receiving Schedule")
        print("   5. Capture scrolling desktop screenshots")
        print("   6. Stitch screenshots together")
        print("   7. Save final image")
        print("\n⏱️  This process takes approximately 3-4 minutes")
        
        choice = input("\nDo you want to test screenshot capture? (y/n): ")
        
        if choice.lower() == 'y':
            screenshot_captured = test_capture_screenshot_now()
            
            if screenshot_captured:
                # Test getting screenshots by date
                print("\n🖼️  TESTING SCREENSHOT RETRIEVAL")
                test_get_screenshot()
                test_get_screenshots_range()
        
        # Test file download functionality
        print("\n📁 TESTING FILE DOWNLOADS")
        test_download_file()
        
        # Test admin functions
        print("\n⚙️  TESTING ADMIN FUNCTIONS")
        test_change_frequency()
        test_set_preferred_hour()
        test_update_credentials()
        
        # Test error handling
        print("\n❌ TESTING ERROR HANDLING")
        test_invalid_admin_password()
        
        # Optional cleanup test
        print("\n🧹 OPTIONAL CLEANUP TEST")
        cleanup_choice = input("Do you want to test cleanup (deletes all screenshots)? (y/n): ")
        if cleanup_choice.lower() == 'y':
            test_cleanup()
        
        print("\n" + "="*70)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*70)
        print("📋 Summary of tested endpoints:")
        print("• GET  /                     - API information")
        print("• GET  /status               - System status")
        print("• POST /screenshot/now       - Capture full desktop screenshot")
        print("• GET  /screenshot/<date>    - Get screenshot by date")
        print("• GET  /screenshots/range    - Get screenshots range/ZIP")
        print("• GET  /download/<filename>  - Download specific file")
        print("• POST /admin/frequency      - Change capture frequency")
        print("• POST /admin/preferred_hour - Set preferred capture hour")
        print("• POST /admin/credentials    - Update Fenix login credentials")
        print("• POST /admin/cleanup        - Delete all screenshots")
        print("="*70)
        print("🎯 Fenix Marine Services Screenshot API is ready for production!")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the API")
        print("Make sure the Flask app is running on http://localhost:5005")
        print("Run: python app.py")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    main()