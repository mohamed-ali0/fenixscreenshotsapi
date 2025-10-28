"""
Diagnostic script to check extension installation on remote server
"""
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

print("="*80)
print("Extension Installation Diagnostic")
print("="*80)

# Check 1: CRX file exists
print("\n[1/5] Checking if gofullpage.crx exists...")
crx_path = os.path.join(os.getcwd(), "gofullpage.crx")
if os.path.exists(crx_path):
    size = os.path.getsize(crx_path)
    print(f"   [OK] Found: {crx_path}")
    print(f"   [OK] Size: {size:,} bytes")
else:
    print(f"   [ERROR] Not found: {crx_path}")
    print(f"   Please download the extension from Chrome Web Store")
    sys.exit(1)

# Check 2: Chrome profile directory
print("\n[2/5] Checking Chrome profile...")
profile_dir = os.path.join(os.getcwd(), "chrome_profile")
if os.path.exists(profile_dir):
    print(f"   [OK] Profile exists: {profile_dir}")
else:
    print(f"   [INFO] Profile will be created: {profile_dir}")

# Check 3: Try loading Chrome with extension
print("\n[3/5] Attempting to load Chrome with extension...")
try:
    chrome_options = Options()
    chrome_options.add_argument(f'--user-data-dir={profile_dir}')
    chrome_options.add_argument('--profile-directory=Default')
    
    # Try to add extension
    try:
        chrome_options.add_extension(crx_path)
        print("   [OK] Extension added to Chrome options")
    except Exception as e:
        print(f"   [ERROR] Failed to add extension: {str(e)}")
    
    # Disable automation flags
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    print("   [INFO] Starting Chrome...")
    driver = webdriver.Chrome(options=chrome_options)
    print("   [OK] Chrome started successfully")
    
    # Check 4: Navigate to extensions page
    print("\n[4/5] Checking installed extensions...")
    driver.get("chrome://extensions/")
    time.sleep(3)
    
    # Get page source to check for extension
    page_source = driver.page_source
    if "GoFullPage" in page_source or "gofullpage" in page_source or "fdpohaocaechififmbbbbbknoalclacl" in page_source:
        print("   [OK] GoFullPage extension detected!")
    else:
        print("   [WARNING] GoFullPage extension NOT detected")
        print("   [INFO] This might mean:")
        print("        - Extension blocked by Chrome policy")
        print("        - Extension blocked by Windows policy")
        print("        - Extension installation requires manual approval")
    
    # Check 5: Test keyboard shortcuts page
    print("\n[5/5] Checking keyboard shortcuts...")
    driver.get("chrome://extensions/shortcuts")
    time.sleep(2)
    
    page_source = driver.page_source
    if "GoFullPage" in page_source:
        print("   [OK] Extension has keyboard shortcuts available")
        if "Alt+Shift+P" in page_source or "⌥⇧P" in page_source:
            print("   [OK] Shortcut Alt+Shift+P is configured!")
        else:
            print("   [WARNING] Shortcut Alt+Shift+P NOT configured")
            print("   [ACTION] Please set it manually at chrome://extensions/shortcuts")
    else:
        print("   [WARNING] Extension shortcuts not available")
    
    print("\n" + "="*80)
    print("Chrome will stay open for 10 seconds for you to inspect...")
    print("Check chrome://extensions/ to see if extension is there")
    print("="*80)
    time.sleep(10)
    
    driver.quit()
    print("\n[COMPLETE] Diagnostic finished")
    
except Exception as e:
    print(f"   [ERROR] Failed to start Chrome: {str(e)}")
    print(f"\nFull error details:")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*80)
print("RECOMMENDATIONS:")
print("="*80)
print("1. If extension is NOT installed:")
print("   → Use Solution 1 from TROUBLESHOOTING_EXTENSION.md")
print("   → Manually install extension once, it will persist")
print("")
print("2. If extension IS installed but shortcut doesn't work:")
print("   → Go to chrome://extensions/shortcuts")
print("   → Set GoFullPage to Alt+Shift+P")
print("")
print("3. If extension is BLOCKED by policy:")
print("   → Use CDP method (Solution 2 in troubleshooting guide)")
print("   → No extension needed, uses Chrome's built-in screenshot")
print("="*80)



