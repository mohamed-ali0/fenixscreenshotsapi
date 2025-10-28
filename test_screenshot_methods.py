#!/usr/bin/env python3
"""
Test script to verify screenshot capture methods work correctly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from automation import (
    capture_desktop_screenshot, 
    capture_screen_win32, 
    capture_screen_mss,
    MSS_AVAILABLE
)
from datetime import datetime
import time

def test_all_screenshot_methods():
    """Test all available screenshot methods"""
    print(f"[{datetime.now()}] Testing screenshot capture methods...")
    print(f"MSS Available: {MSS_AVAILABLE}")
    
    # Test 1: Win32 API Method
    print(f"\n[{datetime.now()}] Testing Win32 API method...")
    try:
        screenshot = capture_screen_win32()
        if screenshot:
            test_filename = f"test_win32_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
            screenshot.save(test_filename)
            print(f"✅ Win32 API screenshot successful: {screenshot.width}x{screenshot.height} -> {test_filename}")
        else:
            print("❌ Win32 API screenshot failed")
    except Exception as e:
        print(f"❌ Win32 API screenshot error: {e}")
    
    # Test 2: MSS Method
    if MSS_AVAILABLE:
        print(f"\n[{datetime.now()}] Testing MSS method...")
        try:
            screenshot = capture_screen_mss()
            if screenshot:
                test_filename = f"test_mss_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
                screenshot.save(test_filename)
                print(f"✅ MSS screenshot successful: {screenshot.width}x{screenshot.height} -> {test_filename}")
            else:
                print("❌ MSS screenshot failed")
        except Exception as e:
            print(f"❌ MSS screenshot error: {e}")
    else:
        print(f"\n[{datetime.now()}] MSS not available - skipping test")
    
    # Test 3: Combined method (without driver for now)
    print(f"\n[{datetime.now()}] Testing combined desktop screenshot method...")
    try:
        screenshot = capture_desktop_screenshot(driver=None)
        if screenshot:
            test_filename = f"test_combined_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
            screenshot.save(test_filename)
            print(f"✅ Combined method screenshot successful: {screenshot.width}x{screenshot.height} -> {test_filename}")
        else:
            print("❌ Combined method screenshot failed")
    except Exception as e:
        print(f"❌ Combined method screenshot error: {e}")

def test_with_browser():
    """Test with an actual browser instance (requires Chrome)"""
    print(f"\n[{datetime.now()}] Testing with browser instance...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        
        # Create driver
        driver = webdriver.Chrome(options=chrome_options)
        
        try:
            # Navigate to a simple page
            driver.get("https://www.google.com")
            time.sleep(3)
            
            # Test combined method with browser
            screenshot = capture_desktop_screenshot(driver=driver)
            if screenshot:
                test_filename = f"test_browser_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
                screenshot.save(test_filename)
                print(f"✅ Browser-based screenshot successful: {screenshot.width}x{screenshot.height} -> {test_filename}")
            else:
                print("❌ Browser-based screenshot failed")
                
        finally:
            driver.quit()
            
    except Exception as e:
        print(f"❌ Browser test error: {e}")
        print("Make sure Chrome is installed and chromedriver is in PATH")

if __name__ == "__main__":
    print("=== Screenshot Methods Test ===")
    
    # Test basic methods
    test_all_screenshot_methods()
    
    # Ask user if they want to test with browser
    print(f"\n[{datetime.now()}] Do you want to test with browser instance? (y/n): ", end="")
    try:
        response = input().lower().strip()
        if response == 'y' or response == 'yes':
            test_with_browser()
    except (EOFError, KeyboardInterrupt):
        print("\nSkipping browser test")
    
    print(f"\n[{datetime.now()}] Screenshot tests completed!")
