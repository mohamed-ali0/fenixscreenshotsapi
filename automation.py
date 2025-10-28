from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import datetime
import os
import glob
from pynput.keyboard import Controller, Key
import win32gui
import win32con
import win32ui
import win32api
import psutil
from PIL import Image, ImageGrab, ImageDraw
import io
try:
    import mss
    MSS_AVAILABLE = True
except ImportError:
    MSS_AVAILABLE = False
    print("MSS not available - install with: pip install mss")


def kill_chrome_process_tree(driver):
    """Kill only the Chrome process created by this driver and its children"""
    try:
        if not driver or not hasattr(driver, 'service') or not driver.service.process:
            return 0
        
        # Get the ChromeDriver service process
        chromedriver_pid = driver.service.process.pid
        
        # Find all child processes (Chrome instances)
        killed_count = 0
        parent = psutil.Process(chromedriver_pid)
        children = parent.children(recursive=True)
        
        # Kill children first (Chrome browser processes)
        for child in children:
            try:
                child.kill()
                killed_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Kill the parent (ChromeDriver)
        try:
            parent.kill()
            killed_count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
        
        if killed_count > 0:
            print(f"[{datetime.now()}] Killed {killed_count} process(es) from this driver")
            time.sleep(1)  # Wait for processes to fully terminate
        
        return killed_count
    except Exception as e:
        print(f"[{datetime.now()}] Error killing driver processes: {str(e)}")
        return 0


def bring_chrome_to_front():
    """Force Chrome window to the front and set to fullscreen using aggressive methods"""
    try:
        def callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_text = win32gui.GetWindowText(hwnd)
                if "Google Chrome" in window_text or "Chrome" in window_text:
                    windows.append(hwnd)
            return True
        
        windows = []
        win32gui.EnumWindows(callback, windows)
        
        if windows:
            # Get the first Chrome window
            hwnd = windows[0]
            
            # Restore if minimized
            try:
                if win32gui.IsIconic(hwnd):
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                    time.sleep(0.2)
            except:
                pass
            
            # Show window normally first
            try:
                win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
                time.sleep(0.1)
            except:
                pass
            
            # Make it topmost temporarily
            try:
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                     win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)
                time.sleep(0.1)
            except:
                pass
            
            # Bring to front
            try:
                win32gui.BringWindowToTop(hwnd)
                time.sleep(0.1)
            except:
                pass
            
            # Set as foreground window
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            
            # Remove topmost flag (so other windows can go on top if needed)
            try:
                win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                                     win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)
                time.sleep(0.1)
            except:
                pass
            
            # Maximize
            try:
                win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            except:
                pass
            
            # Final bring to top
            try:
                win32gui.BringWindowToTop(hwnd)
            except:
                pass
            
            print(f"[{datetime.now()}] Chrome window management completed")
            return True
        
        print(f"[{datetime.now()}] No Chrome window found")
        return False
        
    except Exception as e:
        print(f"[{datetime.now()}] Warning: Error in window management: {str(e)}")
        print(f"[{datetime.now()}] Continuing anyway - automation should still work")
        return False


def find_scroll_target(driver):
    """
    Find the best scroll target element on the page with priority-based selection
    Focus on internal scrollable areas first
    """
    scroll_target = None
    
    # Priority 1: Find internal scrollable areas with significant content
    try:
        js = """
            var scrollables = [];
            var allElements = document.querySelectorAll('*');
            
            for (var i = 0; i < allElements.length; i++) {
                var el = allElements[i];
                var style = window.getComputedStyle(el);
                
                // Check for scrollable content
                if (el.scrollHeight > el.clientHeight + 50 && 
                    (style.overflowY === 'auto' || style.overflowY === 'scroll') &&
                    el.clientHeight > 200) {  // Must be reasonably tall
                    
                    scrollables.push({
                        element: el,
                        scrollHeight: el.scrollHeight,
                        clientHeight: el.clientHeight,
                        scrollRatio: el.scrollHeight / el.clientHeight,
                        className: el.className,
                        tagName: el.tagName
                    });
                }
            }
            
            // Sort by scroll ratio (most scrollable content first)
            scrollables.sort((a, b) => b.scrollRatio - a.scrollRatio);
            
            // Return the element with most scrollable content
            return scrollables.length > 0 ? scrollables[0].element : null;
        """
        scroll_target = driver.execute_script(js)
        if scroll_target:
            # Get element details for debugging
            element_info = driver.execute_script("""
                return {
                    tagName: arguments[0].tagName,
                    className: arguments[0].className,
                    id: arguments[0].id,
                    scrollHeight: arguments[0].scrollHeight,
                    clientHeight: arguments[0].clientHeight,
                    scrollTop: arguments[0].scrollTop
                };
            """, scroll_target)
            print(f"[{datetime.now()}] Found internal scrollable element: {element_info['tagName']}.{element_info['className']} (id: {element_info['id']})")
            print(f"[{datetime.now()}] Scroll dimensions: {element_info['scrollHeight']}px total, {element_info['clientHeight']}px visible")
            return scroll_target
    except Exception as e:
        print(f"[{datetime.now()}] Error finding internal scrollable: {e}")
    
    # Priority 2: Look for common table/grid containers
    try:
        table_selectors = [
            "div[class*='table']",
            "div[class*='grid']", 
            "div[class*='data']",
            "div[class*='content']",
            "div[class*='list']",
            ".ag-root",  # AG Grid
            ".handsontable",  # Handsontable
            "table"
        ]
        
        for selector in table_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed():
                        # Check if this element has scrollable content
                        is_scrollable = driver.execute_script("""
                            var el = arguments[0];
                            return el.scrollHeight > el.clientHeight + 20 && el.clientHeight > 100;
                        """, element)
                        
                        if is_scrollable:
                            scroll_info = driver.execute_script("""
                                return {
                                    scrollHeight: arguments[0].scrollHeight,
                                    clientHeight: arguments[0].clientHeight,
                                    className: arguments[0].className
                                };
                            """, element)
                            print(f"[{datetime.now()}] Found scrollable {selector}: {scroll_info['className']}")
                            print(f"[{datetime.now()}] Dimensions: {scroll_info['scrollHeight']}px total, {scroll_info['clientHeight']}px visible")
                            return element
            except Exception:
                continue
    except Exception:
        pass
    
    # Priority 3: Any element with infinite scroll attribute
    try:
        scroll_target = driver.find_element(By.XPATH, "//*[@matinfinitescroll]")
        if scroll_target and scroll_target.is_displayed():
            print(f"[{datetime.now()}] Found element with matinfinitescroll attribute")
            return scroll_target
    except Exception:
        pass
    
    print(f"[{datetime.now()}] No internal scroll container found, will use window scrolling")
    return None


def perform_scroll(driver, scroll_target=None, scroll_amount=800):
    """
    Perform scrolling with multiple fallback methods and position verification
    """
    # Get initial position
    if scroll_target:
        initial_position = driver.execute_script("return arguments[0].scrollTop;", scroll_target)
    else:
        initial_position = driver.execute_script("return window.pageYOffset || document.documentElement.scrollTop;")
    
    success = False
    
    # Method 1: Element scrollBy (JavaScript - highest priority)
    if scroll_target:
        try:
            driver.execute_script("arguments[0].scrollBy(0, arguments[1]);", scroll_target, scroll_amount)
            # Check if position actually changed
            new_position = driver.execute_script("return arguments[0].scrollTop;", scroll_target)
            if new_position > initial_position:
                success = True
                print(f"[{datetime.now()}] ✅ Element scrollBy successful ({initial_position}px → {new_position}px)")
            else:
                print(f"[{datetime.now()}] ⚠️ Element scrollBy executed but position unchanged ({initial_position}px)")
        except Exception as e:
            print(f"[{datetime.now()}] ⚠️ Element scrollBy failed: {e}")
    
    # Method 2: Window scrollBy (JavaScript fallback)
    if not success:
        try:
            driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_amount)
            new_position = driver.execute_script("return window.pageYOffset || document.documentElement.scrollTop;")
            if new_position > initial_position:
                success = True
                print(f"[{datetime.now()}] ✅ Window scrollBy successful ({initial_position}px → {new_position}px)")
            else:
                print(f"[{datetime.now()}] ⚠️ Window scrollBy executed but position unchanged ({initial_position}px)")
        except Exception as e:
            print(f"[{datetime.now()}] ⚠️ Window scrollBy failed: {e}")
    
    # Method 3: Focus element and use Page Down key
    if not success and scroll_target:
        try:
            # Focus the scrollable element first
            driver.execute_script("arguments[0].focus();", scroll_target)
            actions = ActionChains(driver)
            actions.send_keys(Keys.PAGE_DOWN).perform()
            
            # Check position
            if scroll_target:
                new_position = driver.execute_script("return arguments[0].scrollTop;", scroll_target)
            else:
                new_position = driver.execute_script("return window.pageYOffset || document.documentElement.scrollTop;")
            
            if new_position > initial_position:
                success = True
                print(f"[{datetime.now()}] ✅ Page Down key successful ({initial_position}px → {new_position}px)")
            else:
                print(f"[{datetime.now()}] ⚠️ Page Down executed but position unchanged ({initial_position}px)")
        except Exception as e:
            print(f"[{datetime.now()}] ⚠️ Page Down failed: {e}")
    
    # Method 4: Arrow keys with element focus
    if not success and scroll_target:
        try:
            driver.execute_script("arguments[0].focus();", scroll_target)
            actions = ActionChains(driver)
            actions.send_keys(Keys.ARROW_DOWN * 10).perform()
            
            # Check position
            new_position = driver.execute_script("return arguments[0].scrollTop;", scroll_target)
            if new_position > initial_position:
                success = True
                print(f"[{datetime.now()}] ✅ Arrow keys successful ({initial_position}px → {new_position}px)")
            else:
                print(f"[{datetime.now()}] ⚠️ Arrow keys executed but position unchanged ({initial_position}px)")
        except Exception as e:
            print(f"[{datetime.now()}] ⚠️ Arrow keys failed: {e}")
    
    # Method 5: Mouse wheel scrolling (if supported)
    if not success:
        try:
            actions = ActionChains(driver)
            if scroll_target:
                actions.move_to_element(scroll_target)
            actions.scroll_by_amount(0, scroll_amount).perform()
            
            # Check position
            if scroll_target:
                new_position = driver.execute_script("return arguments[0].scrollTop;", scroll_target)
            else:
                new_position = driver.execute_script("return window.pageYOffset || document.documentElement.scrollTop;")
            
            if new_position > initial_position:
                success = True
                print(f"[{datetime.now()}] ✅ Mouse wheel successful ({initial_position}px → {new_position}px)")
            else:
                print(f"[{datetime.now()}] ⚠️ Mouse wheel executed but position unchanged ({initial_position}px)")
        except Exception as e:
            print(f"[{datetime.now()}] ⚠️ Mouse wheel failed: {e}")
    
    return success


def capture_desktop_screenshot(driver=None):
    """
    Capture desktop screenshot using multiple fallback methods for Windows servers without RDC
    """
    try:
        # Method 1: Try PIL ImageGrab (works when RDC is active)
        try:
            screenshot = ImageGrab.grab()
            print(f"[{datetime.now()}] ✅ ImageGrab screenshot successful")
            return screenshot
        except Exception as e:
            print(f"[{datetime.now()}] ⚠️ ImageGrab failed (expected without RDC): {e}")
    
        # Method 2: MSS (Microsoft Screen Capture) - often works when Win32 fails
        if MSS_AVAILABLE:
            try:
                screenshot = capture_screen_mss()
                if screenshot:
                    print(f"[{datetime.now()}] ✅ MSS screenshot successful")
                    return screenshot
            except Exception as e:
                print(f"[{datetime.now()}] ⚠️ MSS screenshot failed: {e}")
        
        # Method 3: Win32 API screenshot (works without RDC)
        try:
            screenshot = capture_screen_win32()
            if screenshot:
                print(f"[{datetime.now()}] ✅ Win32 API screenshot successful")
                return screenshot
        except Exception as e:
            print(f"[{datetime.now()}] ⚠️ Win32 API screenshot failed: {e}")
        
        # Method 4: Browser-based screenshot with window manipulation
        if driver:
            try:
                screenshot = capture_browser_with_chrome(driver)
                if screenshot:
                    print(f"[{datetime.now()}] ✅ Browser-based screenshot successful")
                    return screenshot
            except Exception as e:
                print(f"[{datetime.now()}] ⚠️ Browser-based screenshot failed: {e}")
        
        print(f"[{datetime.now()}] ❌ All screenshot methods failed")
        return None
        
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Screenshot capture error: {e}")
        return None


def capture_screen_win32():
    """
    Capture screenshot using Win32 API - works without RDC (improved version)
    """
    try:
        # Get screen dimensions
        screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        print(f"[{datetime.now()}] Win32 detected screen: {screen_width}x{screen_height}")
        
        # Try multiple approaches for Win32 screenshot
        
        # Method 1: Desktop window approach
        try:
            hdesktop = win32gui.GetDesktopWindow()
            hwndDC = win32gui.GetWindowDC(hdesktop)
            mfcDC = win32ui.CreateDCFromHandle(hwndDC)
            saveDC = mfcDC.CreateCompatibleDC()
            
            # Create bitmap
            saveBitMap = win32ui.CreateBitmap()
            saveBitMap.CreateCompatibleBitmap(mfcDC, screen_width, screen_height)
            saveDC.SelectObject(saveBitMap)
            
            # Copy screen to bitmap with error checking
            result = saveDC.BitBlt((0, 0), (screen_width, screen_height), mfcDC, (0, 0), win32con.SRCCOPY)
            if not result:
                raise Exception("BitBlt operation failed")
            
            # Convert to PIL Image
            bmpinfo = saveBitMap.GetInfo()
            bmpstr = saveBitMap.GetBitmapBits(True)
            
            screenshot = Image.frombuffer(
                'RGB',
                (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                bmpstr, 'raw', 'BGRX', 0, 1
            )
            
            # Cleanup
            win32gui.DeleteObject(saveBitMap.GetHandle())
            saveDC.DeleteDC()
            mfcDC.DeleteDC()
            win32gui.ReleaseDC(hdesktop, hwndDC)
            
            print(f"[{datetime.now()}] Win32 Method 1 successful: {screenshot.width}x{screenshot.height}")
            return screenshot
            
        except Exception as e1:
            print(f"[{datetime.now()}] Win32 Method 1 failed: {e1}")
        
        # Method 2: Screen DC approach
        try:
            # Get screen DC directly
            hdcScreen = win32gui.GetDC(0)  # Get screen DC
            hdcMemDC = win32gui.CreateCompatibleDC(hdcScreen)
            hbmScreen = win32gui.CreateCompatibleBitmap(hdcScreen, screen_width, screen_height)
            win32gui.SelectObject(hdcMemDC, hbmScreen)
            
            # Copy screen to memory DC
            result = win32gui.BitBlt(hdcMemDC, 0, 0, screen_width, screen_height, hdcScreen, 0, 0, win32con.SRCCOPY)
            if not result:
                raise Exception("BitBlt operation failed on screen DC")
            
            # Get bitmap bits
            bmpinfo = win32gui.GetObject(hbmScreen)
            bmpstr = win32gui.GetBitmapBits(hbmScreen, bmpinfo.bmWidthBytes * bmpinfo.bmHeight)
            
            screenshot = Image.frombuffer(
                'RGB',
                (bmpinfo.bmWidth, bmpinfo.bmHeight),
                bmpstr, 'raw', 'BGRX', 0, 1
            )
            
            # Cleanup
            win32gui.DeleteObject(hbmScreen)
            win32gui.DeleteDC(hdcMemDC)
            win32gui.ReleaseDC(0, hdcScreen)
            
            print(f"[{datetime.now()}] Win32 Method 2 successful: {screenshot.width}x{screenshot.height}")
            return screenshot
            
        except Exception as e2:
            print(f"[{datetime.now()}] Win32 Method 2 failed: {e2}")
        
        print(f"[{datetime.now()}] All Win32 methods failed")
        return None
        
    except Exception as e:
        print(f"[{datetime.now()}] Win32 screenshot general error: {e}")
        return None


def capture_screen_mss():
    """
    Capture screenshot using MSS (Microsoft Screen Capture) - often more reliable than Win32
    """
    if not MSS_AVAILABLE:
        return None
        
    try:
        with mss.mss() as sct:
            # Capture the entire screen
            monitor = sct.monitors[0]  # 0 = all monitors combined
            screenshot_data = sct.grab(monitor)
            
            # Convert to PIL Image
            screenshot = Image.frombytes('RGB', screenshot_data.size, screenshot_data.bgra, 'raw', 'BGRX')
            
            print(f"[{datetime.now()}] MSS screenshot captured: {screenshot.width}x{screenshot.height}")
            return screenshot
            
    except Exception as e:
        print(f"[{datetime.now()}] MSS screenshot error: {e}")
        return None


def capture_browser_with_chrome(driver):
    """
    Capture browser screenshot and create full desktop resolution image with taskbar/desktop context
    """
    try:
        # Get actual screen dimensions first
        try:
            screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
            screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
            print(f"[{datetime.now()}] Desktop resolution detected: {screen_width}x{screen_height}")
        except:
            screen_width = 1920  # Default fallback
            screen_height = 1080
            print(f"[{datetime.now()}] Using fallback resolution: {screen_width}x{screen_height}")
        
        # Try to maximize browser window to get full screen content
        try:
            current_size = driver.get_window_size()
            print(f"[{datetime.now()}] Current browser size: {current_size['width']}x{current_size['height']}")
            
            # Set browser to near full screen (leaving space for taskbar)
            taskbar_height = 40
            target_width = screen_width
            target_height = screen_height - taskbar_height
            
            driver.set_window_position(0, 0)
            driver.set_window_size(target_width, target_height)
            time.sleep(1)  # Wait for resize
            
            new_size = driver.get_window_size()
            print(f"[{datetime.now()}] Resized browser to: {new_size['width']}x{new_size['height']}")
            
        except Exception as e:
            print(f"[{datetime.now()}] Could not resize browser: {e}")
        
        # Get browser screenshot after resize
        screenshot_png = driver.get_screenshot_as_png()
        browser_screenshot = Image.open(io.BytesIO(screenshot_png))
        print(f"[{datetime.now()}] Browser screenshot captured: {browser_screenshot.width}x{browser_screenshot.height}")
        
        # If browser screenshot is close to full screen, return it directly with taskbar
        if browser_screenshot.width >= screen_width * 0.9 and browser_screenshot.height >= (screen_height - 100) * 0.9:
            print(f"[{datetime.now()}] Browser is near full screen, creating minimal desktop simulation")
            
            # Create full desktop image
            desktop_image = Image.new('RGB', (screen_width, screen_height), color=(0, 120, 215))  # Windows blue
            
            # Add taskbar at bottom
            taskbar_height = 40
            taskbar_color = (0, 0, 0)  # Black taskbar
            
            # Draw taskbar more efficiently
            draw = ImageDraw.Draw(desktop_image)
            draw.rectangle([0, screen_height - taskbar_height, screen_width, screen_height], fill=taskbar_color)
            
            # Add start button
            start_button_color = (45, 45, 45)
            draw.rectangle([5, screen_height - taskbar_height + 5, 105, screen_height - 5], fill=start_button_color)
            
            # Paste browser screenshot, scaled to fit if necessary
            if browser_screenshot.width > screen_width or browser_screenshot.height > (screen_height - taskbar_height):
                # Scale down browser screenshot to fit
                max_width = screen_width
                max_height = screen_height - taskbar_height
                browser_screenshot.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                print(f"[{datetime.now()}] Browser screenshot scaled to: {browser_screenshot.width}x{browser_screenshot.height}")
            
            # Center the browser screenshot on desktop
            paste_x = (screen_width - browser_screenshot.width) // 2
            paste_y = max(0, (screen_height - taskbar_height - browser_screenshot.height) // 2)
            
            desktop_image.paste(browser_screenshot, (paste_x, paste_y))
            
            print(f"[{datetime.now()}] Created full desktop simulation: {desktop_image.width}x{desktop_image.height}")
            return desktop_image
        
        else:
            # Browser is small, create full desktop with browser positioned
            print(f"[{datetime.now()}] Browser is small, creating full desktop with positioned browser")
            
            # Create full desktop image
            desktop_image = Image.new('RGB', (screen_width, screen_height), color=(0, 120, 215))  # Windows blue
            
            # Add taskbar
            taskbar_height = 40
            draw = ImageDraw.Draw(desktop_image)
            draw.rectangle([0, screen_height - taskbar_height, screen_width, screen_height], fill=(0, 0, 0))
            draw.rectangle([5, screen_height - taskbar_height + 5, 105, screen_height - 5], fill=(45, 45, 45))
            
            # Get browser window position
            try:
                window_rect = driver.get_window_rect()
                browser_x = max(0, window_rect.get('x', 0))
                browser_y = max(0, window_rect.get('y', 0))
            except:
                browser_x = 0
                browser_y = 0
            
            # Ensure browser fits on desktop
            paste_x = min(browser_x, screen_width - browser_screenshot.width)
            paste_y = min(browser_y, screen_height - browser_screenshot.height - taskbar_height)
            
            desktop_image.paste(browser_screenshot, (paste_x, paste_y))
            
            print(f"[{datetime.now()}] Created positioned desktop: {desktop_image.width}x{desktop_image.height}")
            return desktop_image
        
    except Exception as e:
        print(f"[{datetime.now()}] Browser-based screenshot error: {e}")
        return None


def capture_full_page_screenshot(driver, filename):
    """
    Capture full DESKTOP screenshots by scrolling and stitching images together
    Shows taskbar, URL bar, and complete desktop view - Works without RDC
    """
    try:
        # Create screenshots directory
        screenshots_dir = os.path.join(os.getcwd(), "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)
        
        # Find scroll target first
        scroll_target = find_scroll_target(driver)
        
        # Get dimensions based on scroll target
        if scroll_target:
            # Get dimensions of the scrollable element
            element_info = driver.execute_script("""
                return {
                    scrollHeight: arguments[0].scrollHeight,
                    clientHeight: arguments[0].clientHeight,
                    scrollTop: arguments[0].scrollTop
                };
            """, scroll_target)
            total_height = element_info['scrollHeight']
            viewport_height = element_info['clientHeight']
            print(f"[{datetime.now()}] Using internal scroll container - Total: {total_height}px, Viewport: {viewport_height}px")
        else:
            # Use window dimensions
            total_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
            viewport_height = driver.execute_script("return window.innerHeight")
            print(f"[{datetime.now()}] Using window scrolling - Total: {total_height}px, Viewport: {viewport_height}px")
        
        # Reset scroll position to top
        if scroll_target:
            driver.execute_script("arguments[0].scrollTop = 0;", scroll_target)
        else:
            driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        
        # Calculate scroll amount to avoid duplicate content  
        scroll_amount = int(viewport_height * 0.95)  # 95% of viewport to minimize gaps but avoid major overlap
        screenshots = []
        previous_position = -1
        current_position = 0
        screenshot_count = 0
        no_progress_count = 0
        max_no_progress = 3
        
        print(f"[{datetime.now()}] Starting FULL DESKTOP capture with {scroll_amount}px scroll steps...")
        
        while screenshot_count < 50:  # Safety limit
            screenshot_count += 1
            
            # Get current position
            if scroll_target:
                current_position = driver.execute_script("return arguments[0].scrollTop;", scroll_target)
            else:
                current_position = driver.execute_script("return window.pageYOffset || document.documentElement.scrollTop;")
            
            print(f"[{datetime.now()}] Capturing FULL SCREEN screenshot {screenshot_count} at position {current_position}px")
            
            # Take full desktop screenshot using multiple fallback methods
            screenshot = capture_desktop_screenshot(driver)
            if screenshot:
                screenshots.append(screenshot)
            else:
                print(f"[{datetime.now()}] Failed to capture screenshot {screenshot_count}, stopping")
                break
            
            # Check if we've reached the bottom
            if scroll_target:
                max_scroll = driver.execute_script("return arguments[0].scrollHeight - arguments[0].clientHeight;", scroll_target)
                at_bottom = current_position >= max_scroll - 10  # 10px tolerance
            else:
                at_bottom = driver.execute_script("""
                    return (window.innerHeight + window.scrollY) >= document.body.offsetHeight - 10;
                """)
            
            if at_bottom:
                print(f"[{datetime.now()}] Reached bottom of scrollable content")
                
                # Take one final screenshot after scrolling the ACTUAL outer container to push bottom bars out of view
                print(f"[{datetime.now()}] Finding and scrolling the outer page container to move bottom bars...")
                try:
                    # Try multiple methods to scroll the outer/main page container
                    scroll_methods = [
                        "document.documentElement.scrollTop += 300;",  # Scroll HTML element
                        "document.body.scrollTop += 300;",             # Scroll body element  
                        "window.scrollTo(0, window.scrollY + 300);",   # Window scroll absolute
                        "document.querySelector('html').scrollTop += 300;", # Direct HTML scroll
                        "document.scrollingElement.scrollTop += 300;"  # Standards-compliant scroll
                    ]
                    
                    outer_scrolled = False
                    for i, scroll_js in enumerate(scroll_methods, 1):
                        try:
                            print(f"[{datetime.now()}] Trying outer scroll method {i}: {scroll_js}")
                            initial_scroll = driver.execute_script("return window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0;")
                            
                            driver.execute_script(scroll_js)
                            time.sleep(1)
                            
                            final_scroll = driver.execute_script("return window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0;")
                            
                            if final_scroll > initial_scroll:
                                print(f"[{datetime.now()}] ✅ Outer scroll successful: {initial_scroll}px → {final_scroll}px")
                                outer_scrolled = True
                                break
                            else:
                                print(f"[{datetime.now()}] ⚠️ Outer scroll method {i} failed - no position change")
                        except Exception as e:
                            print(f"[{datetime.now()}] ⚠️ Outer scroll method {i} error: {e}")
                    
                    if outer_scrolled:
                        time.sleep(2)  # Wait for any animations
                        # Take final FULL SCREEN screenshot with bottom bars moved
                        final_screenshot = capture_desktop_screenshot(driver)
                        if final_screenshot:
                            screenshots.append(final_screenshot)
                            screenshot_count += 1
                            print(f"[{datetime.now()}] Captured final FULL SCREEN screenshot {screenshot_count} with bottom bars pushed out of view")
                        else:
                            print(f"[{datetime.now()}] Failed to capture final screenshot")
                    else:
                        print(f"[{datetime.now()}] ⚠️ Could not scroll outer container - bottom bar may still be visible")
                    
                except Exception as e:
                    print(f"[{datetime.now()}] Warning: Could not scroll outer container: {e}")
                
                break
            
            # Check for no progress
            if current_position == previous_position:
                no_progress_count += 1
                print(f"[{datetime.now()}] No scroll progress detected ({no_progress_count}/{max_no_progress})")
                if no_progress_count >= max_no_progress:
                    print(f"[{datetime.now()}] No progress for {max_no_progress} attempts, stopping")
                    break
            else:
                no_progress_count = 0  # Reset counter
            
            # Scroll down
            scroll_success = perform_scroll(driver, scroll_target, scroll_amount)
            if not scroll_success:
                print(f"[{datetime.now()}] All scroll methods failed, stopping capture")
                break
            
            # Wait for scroll and content loading
            time.sleep(2)
            
            # Update previous position for next iteration
            previous_position = current_position
        
        # Stitch images together
        if screenshots:
            print(f"[{datetime.now()}] Stitching {len(screenshots)} screenshots together...")
            final_image = stitch_screenshots(screenshots, scroll_amount)
            
            # Save final image
            final_path = os.path.join(screenshots_dir, filename)
            final_image.save(final_path, "PNG", optimize=True)
            
            # Clean up individual screenshots from memory
            for screenshot in screenshots:
                screenshot.close()
            final_image.close()
            
            print(f"[{datetime.now()}] Full DESKTOP screenshot saved: {final_path}")
            return True, final_path
        else:
            return False, "No screenshots captured"
            
    except Exception as e:
        error_msg = f"Screenshot capture failed: {str(e)}"
        print(f"[{datetime.now()}] {error_msg}")
        return False, error_msg


def stitch_screenshots(screenshots, scroll_amount):
    """
    Simply combine full DESKTOP screenshots vertically - one after another, no offsets
    """
    if not screenshots:
        return None
    
    if len(screenshots) == 1:
        return screenshots[0].copy()
    
    # Get dimensions from first screenshot
    first_screenshot = screenshots[0]
    width = first_screenshot.width
    height_per_screenshot = first_screenshot.height
    
    print(f"[{datetime.now()}] Combining {len(screenshots)} full DESKTOP screenshots vertically...")
    print(f"[{datetime.now()}] Each desktop screenshot: {width}x{height_per_screenshot}px")
    
    # Simple total height = number of screenshots × height of each
    total_height = len(screenshots) * height_per_screenshot
    
    print(f"[{datetime.now()}] Final image: {width}x{total_height}px")
    
    # Create final image
    final_image = Image.new('RGB', (width, total_height), color='white')
    
    # Place each screenshot directly below the previous one
    for i, screenshot in enumerate(screenshots):
        y_position = i * height_per_screenshot
        print(f"[{datetime.now()}] Placing screenshot {i+1} at y={y_position}px")
        final_image.paste(screenshot, (0, y_position))
    
    print(f"[{datetime.now()}] Desktop screenshots combined successfully")
    return final_image


def download_excel_report(username, password):
    """
    Automate login to Fenix Marine Services portal and navigate to Empty Receiving Schedule
    
    Args:
        username: Portal username
        password: Portal password
    
    Returns:
        tuple: (success: bool, message: str)
    """
    driver = None
    
    try:
        # Setup Chrome options - simplified for Fenix Marine Services
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Use persistent user data directory for settings persistence
        user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
        os.makedirs(user_data_dir, exist_ok=True)
        chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
        chrome_options.add_argument('--profile-directory=Default')
        print(f"[{datetime.now()}] Using persistent Chrome profile at: {user_data_dir}")
        
        # Set download preferences
        download_dir = os.path.join(os.getcwd(), "downloads")
        os.makedirs(download_dir, exist_ok=True)
        
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        # Standard automation arguments
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        chrome_options.add_argument('--no-first-run')
        chrome_options.add_argument('--no-service-autorun')
        chrome_options.add_argument('--password-store=basic')
        
        # Uncomment the line below to run in headless mode (without UI)
        # chrome_options.add_argument('--headless=new')
        
        # Initialize the driver
        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Force Chrome window to front ONCE at startup
        print(f"[{datetime.now()}] Forcing Chrome window to front...")
        time.sleep(1)  # Brief wait for window to appear
        bring_chrome_to_front()
        driver.maximize_window()
        print(f"[{datetime.now()}] Chrome window setup complete")
        
        print(f"[{datetime.now()}] Navigating to Fenix Marine Services portal...")
        
        # Navigate to the Fenix Marine Services portal
        driver.get('https://portal.fenixmarineservices.com/apptmt-app/home')
        
        # Wait 30 seconds for page to fully load
        print(f"[{datetime.now()}] Waiting 30s for page to load...")
        time.sleep(30)
        
        # Click the "Login" button (search for button containing "Login" text)
        print(f"[{datetime.now()}] Searching for Login button...")
        login_button = None
        
        # Try multiple selectors to find the Login button specifically
        login_selectors = [
            "//button[contains(text(), 'Login')]",
            "//button[@class='button' and contains(text(), 'Login')]",
            "//button[text()='Login']",
            "//input[@value='Login']",
            "//a[contains(text(), 'Login')]"
        ]
        
        for selector in login_selectors:
            try:
                login_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                print(f"[{datetime.now()}] Found Login button with selector: {selector}")
                break
            except:
                continue
        
        if login_button:
            print(f"[{datetime.now()}] Clicking Login button...")
            login_button.click()
        else:
            print(f"[{datetime.now()}] Login button not found, trying generic button.button selector...")
            # Fallback to original selector if specific login text not found
            login_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button"))
            )
            login_button.click()
        
        # Wait 15 seconds for login page to load
        print(f"[{datetime.now()}] Waiting 15s for login page...")
        time.sleep(15)
        
        # Enter username with autofill clearing
        print(f"[{datetime.now()}] Clearing and entering username...")
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        
        # Clear any autofilled content thoroughly
        current_value = username_field.get_attribute('value')
        if current_value:
            print(f"[{datetime.now()}] Detected autofilled username: '{current_value}', clearing...")
            
        # Multiple clearing methods to ensure field is empty
        username_field.clear()
        username_field.send_keys(Keys.CONTROL + "a")  # Select all
        username_field.send_keys(Keys.DELETE)  # Delete selection
        time.sleep(0.5)  # Brief pause
        
        # Verify field is empty and enter username
        final_value = username_field.get_attribute('value')
        if final_value:
            print(f"[{datetime.now()}] Warning: Username field still contains: '{final_value}'")
            # Force clear with JavaScript
            driver.execute_script("arguments[0].value = '';", username_field)
        
        username_field.send_keys(username)
        print(f"[{datetime.now()}] Username entered successfully")
        
        # Enter password with autofill clearing  
        print(f"[{datetime.now()}] Clearing and entering password...")
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        
        # Clear any autofilled content thoroughly
        current_pwd_value = password_field.get_attribute('value')
        if current_pwd_value:
            print(f"[{datetime.now()}] Detected autofilled password, clearing...")
            
        # Multiple clearing methods to ensure field is empty
        password_field.clear()
        password_field.send_keys(Keys.CONTROL + "a")  # Select all
        password_field.send_keys(Keys.DELETE)  # Delete selection
        time.sleep(0.5)  # Brief pause
        
        # Verify field is empty and enter password
        final_pwd_value = password_field.get_attribute('value')
        if final_pwd_value:
            print(f"[{datetime.now()}] Warning: Password field still contains content, force clearing...")
            # Force clear with JavaScript
            driver.execute_script("arguments[0].value = '';", password_field)
        
        password_field.send_keys(password)
        print(f"[{datetime.now()}] Password entered successfully")
        
        # Click the terms and conditions checkbox
        print(f"[{datetime.now()}] Clicking terms and conditions checkbox...")
        checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "toggle-tnc"))
        )
        checkbox.click()
        
        # Click "Sign In" button
        print(f"[{datetime.now()}] Clicking Sign In button...")
        signin_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "kc-login"))
        )
        signin_button.click()
        
        # Wait 30 seconds for page to fully load after login
        print(f"[{datetime.now()}] Waiting 30s for page to load after login...")
        time.sleep(30)
        
        # Expand "FMS Terminal Schedule" in left sidebar
        print(f"[{datetime.now()}] Looking for FMS Terminal Schedule in sidebar...")
        try:
            # Try multiple selectors for the FMS Terminal Schedule item
            fms_selectors = [
                "//span[contains(text(), 'FMS Terminal Schedule')]",
                "//a[contains(text(), 'FMS Terminal Schedule')]",
                "//div[contains(text(), 'FMS Terminal Schedule')]",
                "//*[contains(text(), 'FMS Terminal Schedule')]"
            ]
            
            fms_element = None
            for selector in fms_selectors:
                try:
                    fms_element = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    print(f"[{datetime.now()}] Found FMS Terminal Schedule with selector: {selector}")
                    break
                except:
                    continue
            
            if fms_element:
                print(f"[{datetime.now()}] Expanding FMS Terminal Schedule...")
                fms_element.click()
                time.sleep(2)  # Brief wait for expansion
            else:
                print(f"[{datetime.now()}] FMS Terminal Schedule not found, continuing...")
                
        except Exception as e:
            print(f"[{datetime.now()}] Error expanding FMS Terminal Schedule: {str(e)}")
            print(f"[{datetime.now()}] Continuing anyway...")
        
        # Click "Empty Receiving Schedule"
        print(f"[{datetime.now()}] Looking for Empty Receiving Schedule...")
        try:
            # Try multiple selectors for Empty Receiving Schedule
            empty_receiving_selectors = [
                "//span[contains(text(), 'Empty Receiving Schedule')]",
                "//a[contains(text(), 'Empty Receiving Schedule')]",
                "//div[contains(text(), 'Empty Receiving Schedule')]",
                "//*[contains(text(), 'Empty Receiving Schedule')]"
            ]
            
            empty_receiving_element = None
            for selector in empty_receiving_selectors:
                try:
                    empty_receiving_element = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    print(f"[{datetime.now()}] Found Empty Receiving Schedule with selector: {selector}")
                    break
                except:
                    continue
            
            if empty_receiving_element:
                print(f"[{datetime.now()}] Clicking Empty Receiving Schedule...")
                empty_receiving_element.click()
                print(f"[{datetime.now()}] Successfully navigated to Empty Receiving Schedule")
                time.sleep(5)  # Wait for page to load
            else:
                raise Exception("Could not find Empty Receiving Schedule")
                
        except Exception as e:
            print(f"[{datetime.now()}] Error: Could not find or click Empty Receiving Schedule: {str(e)}")
            raise Exception(f"Could not find Empty Receiving Schedule: {str(e)}")
        
        # Successfully navigated to Empty Receiving Schedule page
        print(f"[{datetime.now()}] Successfully completed navigation to Empty Receiving Schedule")
        
        # Wait 15 seconds before starting screenshot process
        print(f"[{datetime.now()}] Waiting 15 seconds before capturing screenshots...")
        time.sleep(15)
        
        # Capture full page screenshot with scrolling
        timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_filename = f"fenix_screenshot_{timestamp}.png"
        
        success, screenshot_path = capture_full_page_screenshot(driver, screenshot_filename)
        
        if success:
            return True, f"Successfully captured full DESKTOP screenshot: {screenshot_path}"
        else:
            return False, f"Navigation successful but desktop screenshot failed: {screenshot_path}"
    
    except Exception as e:
        error_msg = f"Error navigating to Fenix Marine Services: {str(e)}"
        print(f"[{datetime.now()}] {error_msg}")
        return False, error_msg
    
    finally:
        # Close the browser
        if driver:
            try:
                # First try graceful shutdown
                driver.quit()
                print(f"[{datetime.now()}] Browser quit() called")
                time.sleep(1)  # Brief wait for quit() to complete
                
                # Force kill to ensure complete cleanup (prevents profile lock)
                print(f"[{datetime.now()}] Ensuring process cleanup...")
                killed = kill_chrome_process_tree(driver)
                if killed > 0:
                    print(f"[{datetime.now()}] Cleaned up {killed} remaining process(es)")
                    
            except Exception as e:
                print(f"[{datetime.now()}] Error during cleanup: {str(e)}")
                # Try to kill process tree as last resort
                try:
                    kill_chrome_process_tree(driver)
                except:
                    pass
            
        print(f"[{datetime.now()}] Cleanup complete")


if __name__ == "__main__":
    # Test the automation
    print("Testing Fenix Marine Services automation...")
    from system_settings import SystemSettings
    
    settings = SystemSettings()
    credentials = settings.get_login_credentials()
    
    success, message = download_excel_report(
        credentials['username'], 
        credentials['password']
    )
    
    if success:
        print(f"✓ Success: {message}")
    else:
        print(f"✗ Failed: {message}")

