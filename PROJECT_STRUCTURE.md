# 📁 Project Structure

## 🎯 **Organized Project Layout**

The project has been reorganized into a clean, logical structure:

```
portoptimizer_screenshot_api/
├── 📁 tester/                    # All test and utility scripts
├── 📁 documentation/             # All documentation and batch files
├── 📁 chrome_profile/            # Chrome browser profile
├── 📁 downloads/                 # Downloaded Excel and PDF files
├── 📁 screenshots/               # Legacy screenshot files
├── 📁 gofullpage_source/         # GoFullPage extension source
├── 📄 app.py                     # Main Flask application
├── 📄 automation.py              # Selenium automation logic
├── 📄 system_settings.py         # Settings management
├── 📄 system_settings.json       # Settings configuration
├── 📄 requirements.txt           # Python dependencies
├── 📄 PortOptimizer_API.postman_collection.json
├── 📄 PortOptimizer_API.postman_environment.json
└── 📄 gofullpage.crx            # Chrome extension
```

---

## 📁 **tester/ Folder**

Contains all test scripts and utility tools:

### **🧪 Test Scripts:**
- `test_api.py` - Complete API test suite
- `test_excel_download.py` - Excel download testing
- `test_pdf_conversion.py` - PDF conversion testing
- `test_settings.py` - Settings validation
- `test_utc_naming.py` - UTC timestamp testing
- `test_*.py` - Various other test scripts

### **🔧 Conversion Tools:**
- `convert_existing_excel.py` - Convert existing Excel files
- `convert_specific.py` - Convert specific Excel file
- `convert_latest.py` - Convert most recent Excel file
- `quick_pdf.py` - Quick PDF conversion
- `simple_excel_to_pdf.py` - Simple Excel to PDF
- `print_to_pdf.py` - Print to PDF utility

### **📊 Report Generators:**
- `create_container_report.py` - Container report generator
- `create_structured_report.py` - Structured report generator
- `convert_excel_to_proper_format.py` - Format converter

### **🛠️ Utilities:**
- `list_and_convert.py` - List and convert files
- `run_excel_test.py` - Excel test runner

---

## 📁 **documentation/ Folder**

Contains all documentation and batch files:

### **📖 Documentation:**
- `README.md` - Main project documentation
- `API_ENDPOINTS.md` - Complete API reference
- `POSTMAN_GUIDE.md` - Postman testing guide
- `QUICK_START.md` - Quick start guide
- `EXCEL_DOWNLOAD_APPROACH.md` - Excel download approach
- `FIRST_RUN_SETUP.md` - First run setup
- `INSTALL_AS_SERVICE.md` - Service installation
- `MANUAL_SETUP_REMOTE_SERVER.md` - Remote server setup
- `QUICK_START_REMOTE_SERVER.md` - Quick remote setup
- `SETUP_GOFULLPAGE.md` - GoFullPage setup
- `TEST_API_README.md` - API testing guide
- `TROUBLESHOOTING_EXTENSION.md` - Extension troubleshooting
- `WINDOWS_FOREGROUND_FIX.md` - Windows focus fixes
- `DISABLE_WINDOWS_FOCUS_BLOCK.md` - Focus block disabling
- `ENABLE_BACKGROUND_KEYBOARD.md` - Background keyboard
- `WINDOWS_FOREGROUND_FIX.md` - Foreground window fixes
- `CHANGELOG.md` - Project changelog

### **🔧 Batch Files:**
- `run.bat` - Run the application
- `start_service.bat` - Start as service
- `excel_to_pdf.bat` - Excel to PDF conversion
- `excel_to_pdf_simple.bat` - Simple Excel to PDF
- `install_pynput.bat` - Install pynput library

---

## 🎯 **Main Directory**

Contains only the essential production files:

### **🚀 Core Application:**
- `app.py` - Main Flask API server
- `automation.py` - Selenium automation
- `system_settings.py` - Settings management
- `system_settings.json` - Configuration

### **📦 Dependencies:**
- `requirements.txt` - Python packages
- `requirements_test.txt` - Test packages

### **🌐 API Testing:**
- `PortOptimizer_API.postman_collection.json` - Postman collection
- `PortOptimizer_API.postman_environment.json` - Postman environment

### **🔧 Utilities:**
- `check_extension.py` - Extension checker
- `install_pdf_libraries.py` - PDF library installer
- `install_service.ps1` - Service installer
- `enable_background_keyboard.ps1` - Keyboard enabler

### **🌐 Browser:**
- `gofullpage.crx` - Chrome extension
- `chrome_profile/` - Browser profile
- `gofullpage_source/` - Extension source

### **📁 Data Directories:**
- `downloads/` - Excel and PDF files
- `screenshots/` - Legacy screenshots

---

## ✅ **Benefits of This Organization**

### **🧹 Clean Main Directory:**
- Only essential production files in root
- Easy to find core application files
- Clear separation of concerns

### **📁 Logical Grouping:**
- All test scripts in `tester/`
- All documentation in `documentation/`
- Easy to navigate and maintain

### **🔍 Easy Discovery:**
- Test scripts grouped together
- Documentation centralized
- Batch files organized

### **🚀 Production Ready:**
- Clean deployment structure
- Essential files easily accessible
- Test files separated from production

---

## 🎯 **Usage**

### **To run tests:**
```bash
cd tester
python test_api.py
```

### **To view documentation:**
```bash
cd documentation
# Open any .md file
```

### **To run the application:**
```bash
python app.py
```

This organization makes the project much cleaner and easier to navigate! 🎯

