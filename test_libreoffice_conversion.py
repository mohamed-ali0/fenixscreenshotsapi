import os
import subprocess
from datetime import datetime

def test_libreoffice_available():
    """Test if LibreOffice is available on the system"""
    try:
        result = subprocess.run(['libreoffice', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"SUCCESS: LibreOffice found: {result.stdout.strip()}")
            return True
        else:
            print(f"ERROR: LibreOffice error: {result.stderr}")
            return False
    except FileNotFoundError:
        print("ERROR: LibreOffice not found - not installed")
        return False
    except subprocess.TimeoutExpired:
        print("ERROR: LibreOffice command timed out")
        return False
    except Exception as e:
        print(f"ERROR: Error checking LibreOffice: {str(e)}")
        return False

def test_excel_file_exists():
    """Test if we have an Excel file to convert"""
    downloads_dir = "downloads"
    if not os.path.exists(downloads_dir):
        print("ERROR: Downloads directory not found")
        return None
    
    excel_files = []
    for filename in os.listdir(downloads_dir):
        if filename.endswith(('.xlsx', '.xls')) and not filename.startswith('~$'):
            excel_files.append(filename)
    
    if not excel_files:
        print("ERROR: No Excel files found in downloads directory")
        return None
    
    # Get the most recent file
    latest_file = max(excel_files, key=lambda x: os.path.getctime(os.path.join(downloads_dir, x)))
    excel_path = os.path.join(downloads_dir, latest_file)
    
    print(f"SUCCESS: Found Excel file: {latest_file}")
    return excel_path

def test_libreoffice_conversion(excel_path):
    """Test LibreOffice conversion"""
    try:
        print(f"\nTesting LibreOffice conversion...")
        print(f"Input: {excel_path}")
        
        # Create test output directory
        test_output_dir = "test_pdf_output"
        os.makedirs(test_output_dir, exist_ok=True)
        
        # Expected output path
        excel_name = os.path.splitext(os.path.basename(excel_path))[0]
        pdf_path = os.path.join(test_output_dir, f"{excel_name}.pdf")
        
        print(f"Output: {pdf_path}")
        
        # LibreOffice command
        cmd = [
            'libreoffice',
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', test_output_dir,
            '--infilter=calc8',
            excel_path
        ]
        
        print(f"Command: {' '.join(cmd)}")
        
        # Run conversion
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        print(f"Return code: {result.returncode}")
        if result.stdout:
            print(f"STDOUT: {result.stdout}")
        if result.stderr:
            print(f"STDERR: {result.stderr}")
        
        if result.returncode == 0:
            if os.path.exists(pdf_path):
                file_size = os.path.getsize(pdf_path)
                print(f"SUCCESS: PDF created successfully!")
                print(f"File: {pdf_path}")
                print(f"Size: {file_size} bytes")
                return True
            else:
                print("ERROR: PDF file not found after conversion")
                return False
        else:
            print("ERROR: LibreOffice conversion failed")
            return False
            
    except subprocess.TimeoutExpired:
        print("ERROR: Conversion timed out")
        return False
    except Exception as e:
        print(f"ERROR: Error during conversion: {str(e)}")
        return False

def test_python_libraries():
    """Test if required Python libraries are available"""
    print(f"\nTesting Python libraries...")
    
    try:
        import pandas as pd
        print("SUCCESS: pandas available")
    except ImportError:
        print("ERROR: pandas not available")
        return False
    
    try:
        import reportlab
        print("SUCCESS: reportlab available")
    except ImportError:
        print("ERROR: reportlab not available")
        return False
    
    try:
        import openpyxl
        print("SUCCESS: openpyxl available")
    except ImportError:
        print("ERROR: openpyxl not available")
        return False
    
    return True

def main():
    print("=" * 60)
    print("TESTING PDF CONVERSION METHODS")
    print("=" * 60)
    
    # Test 1: Check LibreOffice availability
    print("\n1. Testing LibreOffice availability...")
    libreoffice_available = test_libreoffice_available()
    
    # Test 2: Check Excel file
    print("\n2. Testing Excel file availability...")
    excel_path = test_excel_file_exists()
    
    # Test 3: Test LibreOffice conversion
    if libreoffice_available and excel_path:
        print("\n3. Testing LibreOffice conversion...")
        conversion_success = test_libreoffice_conversion(excel_path)
    else:
        print("\n3. Skipping LibreOffice conversion test")
        conversion_success = False
    
    # Test 4: Check Python libraries
    print("\n4. Testing Python libraries...")
    python_libs_available = test_python_libraries()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    print(f"LibreOffice available: {'YES' if libreoffice_available else 'NO'}")
    print(f"Excel file found: {'YES' if excel_path else 'NO'}")
    print(f"LibreOffice conversion: {'YES' if conversion_success else 'NO'}")
    print(f"Python libraries: {'YES' if python_libs_available else 'NO'}")
    
    if conversion_success:
        print("\nSUCCESS: LibreOffice conversion works!")
        print("You can use LibreOffice for PDF conversion without Excel.")
    elif python_libs_available:
        print("\nWARNING: LibreOffice failed, but Python libraries available.")
        print("You can use Python libraries as fallback.")
    else:
        print("\nFAILURE: No working PDF conversion method found.")
        print("You need to either:")
        print("1. Install LibreOffice")
        print("2. Install Python libraries: pip install pandas reportlab openpyxl")
        print("3. Install Microsoft Excel")

if __name__ == "__main__":
    main()
