# Fenix Marine Services Screenshot API - cURL Test Commands

This document contains cURL commands to test all API endpoints using the remote server.

**Remote Server:** `37.60.243.201:5005`  
**Base URL:** `http://37.60.243.201:5005`  
**Admin Password:** `YB02Ss3JJdk`

---

## 1. API Information (Root Endpoint)

Get API information and available endpoints.

```bash
curl -X GET http://37.60.243.201:5005/
```

**Expected Response:**
```json
{
  "name": "Fenix Marine Services Screenshot API",
  "version": "2.0.0",
  "endpoints": { ... }
}
```

---

## 2. System Status

Get current system status, statistics, and configuration.

```bash
curl -X GET http://37.60.243.201:5005/status
```

**Expected Response:**
```json
{
  "success": true,
  "system_info": { ... },
  "scheduler_info": { ... },
  "credentials": { ... },
  "screenshot_stats": { ... }
}
```

---

## 3. Get Screenshot by Date

Retrieve a screenshot for a specific date (format: YYYY-MM-DD).

```bash
# Get screenshot for a specific date
curl -X GET "http://37.60.243.201:5005/screenshot/2025-10-28"
```

**Example with Today's Date:**
```bash
curl -X GET "http://37.60.243.201:5005/screenshot/$(date +%Y-%m-%d)"
```

**Expected Response:**
```json
{
  "success": true,
  "date": "2025-10-28",
  "filename": "fenix_screenshot_2025-10-28_22-16-30.png",
  "download_url": "http://37.60.243.201:5005/download/fenix_screenshot_2025-10-28_22-16-30.png",
  "message": "Screenshot found for 2025-10-28"
}
```

---

## 4. Get Screenshots Range

Get screenshots within a date range or the last N screenshots.

### Get Last N Screenshots

```bash
# Get last 5 screenshots
curl -X GET "http://37.60.243.201:5005/screenshots/range?last_n=5"
```

### Get Screenshots by Date Range

```bash
# Get screenshots from start_date to end_date
curl -X GET "http://37.60.243.201:5005/screenshots/range?start_date=2025-10-01&end_date=2025-10-31"
```

**Expected Response:**
```json
{
  "success": true,
  "zip_filename": "screenshots_20251029_120000.zip",
  "download_url": "http://37.60.243.201:5005/download/screenshots_20251029_120000.zip",
  "screenshot_count": 5,
  "screenshots": [ ... ],
  "message": "ZIP file created with 5 screenshot(s)"
}
```

---

## 5. Download Screenshot File

Download a specific screenshot file by filename.

```bash
# Download a specific screenshot file
curl -X GET "http://37.60.243.201:5005/download/fenix_screenshot_2025-10-28_22-16-30.png" -o screenshot.png

# Or download with original filename
curl -X GET "http://37.60.243.201:5005/download/fenix_screenshot_2025-10-28_22-16-30.png" --remote-name --remote-header-name
```

**With Progress Bar:**
```bash
curl -X GET "http://37.60.243.201:5005/download/fenix_screenshot_2025-10-28_22-16-30.png" --progress-bar -o screenshot.png
```

---

## 6. Capture Screenshot Now

Trigger an immediate screenshot capture (requires admin password).

```bash
curl -X POST http://37.60.243.201:5005/screenshot/now \
  -H "Content-Type: application/json" \
  -d '{
    "admin_password": "YB02Ss3JJdk"
  }'
```

**Formatted (Pretty Print):**
```bash
curl -X POST http://37.60.243.201:5005/screenshot/now \
  -H "Content-Type: application/json" \
  -d '{
    "admin_password": "YB02Ss3JJdk"
  }' | python -m json.tool
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Fenix Marine Services screenshot captured successfully",
  "filename": "fenix_screenshot_2025-10-29_12-00-00.png",
  "download_url": "http://37.60.243.201:5005/download/fenix_screenshot_2025-10-29_12-00-00.png"
}
```

---

## 7. Change Screenshot Frequency

Update the frequency of automated screenshot captures (requires admin password).

```bash
# Change frequency to 12 hours
curl -X POST http://37.60.243.201:5005/admin/frequency \
  -H "Content-Type: application/json" \
  -d '{
    "admin_password": "YB02Ss3JJdk",
    "frequency_hours": 12
  }'

# Change frequency to 24 hours (default)
curl -X POST http://37.60.243.201:5005/admin/frequency \
  -H "Content-Type: application/json" \
  -d '{
    "admin_password": "YB02Ss3JJdk",
    "frequency_hours": 24
  }'

# Change frequency to 6 hours
curl -X POST http://37.60.243.201:5005/admin/frequency \
  -H "Content-Type: application/json" \
  -d '{
    "admin_password": "YB02Ss3JJdk",
    "frequency_hours": 6
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Frequency updated to 12 hours",
  "frequency_hours": 12
}
```

---

## 8. Set Preferred Hour

Set the preferred hour for scheduled screenshot captures (requires admin password).

```bash
# Set preferred hour to 10:00 AM (hour 10)
curl -X POST http://37.60.243.201:5005/admin/preferred_hour \
  -H "Content-Type: application/json" \
  -d '{
    "admin_password": "YB02Ss3JJdk",
    "preferred_hour": 10
  }'

# Set preferred hour to 2:00 AM (hour 2)
curl -X POST http://37.60.243.201:5005/admin/preferred_hour \
  -H "Content-Type: application/json" \
  -d '{
    "admin_password": "YB02Ss3JJdk",
    "preferred_hour": 2
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Preferred hour updated to 10:00",
  "preferred_hour": 10
}
```

---

## 9. Update Login Credentials

Update the Fenix Marine Services portal login credentials (requires admin password).

```bash
curl -X POST http://37.60.243.201:5005/admin/credentials \
  -H "Content-Type: application/json" \
  -d '{
    "admin_password": "YB02Ss3JJdk",
    "username": "your_username",
    "password": "your_password"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Login credentials updated successfully"
}
```

---

## 10. Cleanup (Delete All Screenshots)

Delete all screenshot files (requires admin password).

⚠️ **Warning:** This action cannot be undone!

```bash
curl -X POST http://37.60.243.201:5005/admin/cleanup \
  -H "Content-Type: application/json" \
  -d '{
    "admin_password": "YB02Ss3JJdk"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Cleanup completed. 15 files deleted."
}
```

---

## Complete Test Sequence

Here's a complete sequence to test all endpoints:

```bash
#!/bin/bash

# Configuration
BASE_URL="http://37.60.243.201:5005"
ADMIN_PASSWORD="YB02Ss3JJdk"

echo "=== Testing Fenix Marine Services Screenshot API ==="
echo ""

# 1. Get API Information
echo "1. Getting API information..."
curl -s "$BASE_URL/" | python -m json.tool
echo ""

# 2. Get System Status
echo "2. Getting system status..."
curl -s "$BASE_URL/status" | python -m json.tool
echo ""

# 3. Capture Screenshot Now
echo "3. Capturing screenshot now..."
SCREENSHOT_RESPONSE=$(curl -s -X POST "$BASE_URL/screenshot/now" \
  -H "Content-Type: application/json" \
  -d "{\"admin_password\": \"$ADMIN_PASSWORD\"}")
echo "$SCREENSHOT_RESPONSE" | python -m json.tool
echo ""

# Extract filename from response (requires jq or manual parsing)
# FILENAME=$(echo "$SCREENSHOT_RESPONSE" | jq -r '.filename')

# 4. Get Screenshot by Date
echo "4. Getting today's screenshot..."
TODAY=$(date +%Y-%m-%d)
curl -s "$BASE_URL/screenshot/$TODAY" | python -m json.tool
echo ""

# 5. Get Last 5 Screenshots
echo "5. Getting last 5 screenshots..."
curl -s "$BASE_URL/screenshots/range?last_n=5" | python -m json.tool
echo ""

# 6. Get Screenshots Range
echo "6. Getting screenshots in date range..."
START_DATE=$(date -d "7 days ago" +%Y-%m-%d)
END_DATE=$(date +%Y-%m-%d)
curl -s "$BASE_URL/screenshots/range?start_date=$START_DATE&end_date=$END_DATE" | python -m json.tool
echo ""

# 7. Change Frequency
echo "7. Changing frequency to 12 hours..."
curl -s -X POST "$BASE_URL/admin/frequency" \
  -H "Content-Type: application/json" \
  -d "{\"admin_password\": \"$ADMIN_PASSWORD\", \"frequency_hours\": 12}" | python -m json.tool
echo ""

# 8. Set Preferred Hour
echo "8. Setting preferred hour to 10:00..."
curl -s -X POST "$BASE_URL/admin/preferred_hour" \
  -H "Content-Type: application/json" \
  -d "{\"admin_password\": \"$ADMIN_PASSWORD\", \"preferred_hour\": 10}" | python -m json.tool
echo ""

echo "=== Test sequence completed ==="
```

Save this as `test_api.sh`, make it executable (`chmod +x test_api.sh`), and run it to test all endpoints.

---

## Error Handling Examples

### Invalid Date Format
```bash
curl -X GET "http://37.60.243.201:5005/screenshot/2025-13-45"
```

**Expected Response (400 Bad Request):**
```json
{
  "success": false,
  "error": "Invalid date format. Use YYYY-MM-DD"
}
```

### Invalid Admin Password
```bash
curl -X POST http://37.60.243.201:5005/screenshot/now \
  -H "Content-Type: application/json" \
  -d '{
    "admin_password": "wrong_password"
  }'
```

**Expected Response (403 Forbidden):**
```json
{
  "success": false,
  "error": "Invalid admin password"
}
```

### Missing Required Fields
```bash
curl -X POST http://37.60.243.201:5005/admin/frequency \
  -H "Content-Type: application/json" \
  -d '{
    "frequency_hours": 12
  }'
```

**Expected Response (400 Bad Request):**
```json
{
  "success": false,
  "error": "admin_password and frequency_hours are required"
}
```

---

## Tips and Best Practices

1. **Pretty Print JSON:** Pipe responses through `python -m json.tool` or `jq` for formatted output
   ```bash
   curl -s "$BASE_URL/status" | python -m json.tool
   ```

2. **Save Responses:** Use `-o filename.json` to save responses
   ```bash
   curl -s "$BASE_URL/status" -o status_response.json
   ```

3. **Verbose Mode:** Use `-v` flag to see request/response headers
   ```bash
   curl -v "$BASE_URL/status"
   ```

4. **Follow Redirects:** Use `-L` flag if redirects are encountered
   ```bash
   curl -L "$BASE_URL/download/filename.png" -o screenshot.png
   ```

5. **Timeout Settings:** Use `--max-time` to set request timeout
   ```bash
   curl --max-time 300 "$BASE_URL/screenshot/now" ...
   ```

6. **Progress Bar:** Use `--progress-bar` for download progress
   ```bash
   curl --progress-bar "$BASE_URL/download/filename.png" -o screenshot.png
   ```

---

## Notes

- All timestamps are in server timezone
- Screenshot filenames follow the pattern: `fenix_screenshot_YYYY-MM-DD_HH-MM-SS.png`
- Date format must be: `YYYY-MM-DD` (e.g., `2025-10-29`)
- Admin password is required for all `/admin/*` endpoints and `/screenshot/now`
- The API runs on port `5005` on the remote server
- All screenshot files are stored in the `screenshots/` directory on the server

---

## Quick Reference

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/` | GET | No | API information |
| `/status` | GET | No | System status |
| `/screenshot/<date>` | GET | No | Get screenshot by date |
| `/screenshots/range` | GET | No | Get screenshots range |
| `/download/<filename>` | GET | No | Download file |
| `/screenshot/now` | POST | Yes | Capture screenshot now |
| `/admin/frequency` | POST | Yes | Change frequency |
| `/admin/preferred_hour` | POST | Yes | Set preferred hour |
| `/admin/credentials` | POST | Yes | Update credentials |
| `/admin/cleanup` | POST | Yes | Delete all screenshots |

