import os
import subprocess
import sys
from datetime import datetime

def test_methods():
    """Test PDF conversion methods without crashing on errors"""
    print("="*60)
    print("PDF CONVERSION METHODS TEST")
    print("="*60)
    
    methods = {}
    
    # Method 1: Python Libraries (pandas + reportlab)
    print("\n1. Python Libraries (pandas + reportlab)...")
    try:
        import pandas as pd
        from reportlab.lib.pagesizes import letter, landscape
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
        from reportlab.lib import colors
        methods["Python Libraries"] = True
        print("   SUCCESS: Available")
    except Exception as e:
        methods["Python Libraries"] = False
        print(f"   ERROR: {str(e)[:50]}...")
    
    # Method 2: Matplotlib
    print("\n2. Matplotlib...")
    try:
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_pdf import PdfPages
        methods["Matplotlib"] = True
        print("   SUCCESS: Available")
    except Exception as e:
        methods["Matplotlib"] = False
        print(f"   ERROR: {str(e)[:50]}...")
    
    # Method 3: WeasyPrint (with error handling)
    print("\n3. WeasyPrint...")
    try:
        import weasyprint
        methods["WeasyPrint"] = True
        print("   SUCCESS: Available")
    except Exception as e:
        methods["WeasyPrint"] = False
        print(f"   ERROR: Missing dependencies")
    
    # Method 4: pdfkit
    print("\n4. pdfkit...")
    try:
        import pdfkit
        methods["pdfkit"] = True
        print("   SUCCESS: Available")
    except Exception as e:
        methods["pdfkit"] = False
        print(f"   ERROR: Not installed")
    
    # Method 5: pywin32 (Windows COM)
    print("\n5. pywin32 (Windows COM)...")
    try:
        import win32com.client
        methods["pywin32"] = True
        print("   SUCCESS: Available")
    except Exception as e:
        methods["pywin32"] = False
        print(f"   ERROR: Not installed")
    
    # Method 6: LibreOffice
    print("\n6. LibreOffice...")
    try:
        result = subprocess.run(['libreoffice', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            methods["LibreOffice"] = True
            print("   SUCCESS: Available")
        else:
            methods["LibreOffice"] = False
            print("   ERROR: Not working")
    except Exception as e:
        methods["LibreOffice"] = False
        print("   ERROR: Not installed")
    
    # Method 7: Microsoft Excel (via COM)
    print("\n7. Microsoft Excel...")
    try:
        import win32com.client
        excel = win32com.client.Dispatch("Excel.Application")
        excel.Visible = False
        excel.Quit()
        methods["Microsoft Excel"] = True
        print("   SUCCESS: Available")
    except Exception as e:
        methods["Microsoft Excel"] = False
        print("   ERROR: Not available")
    
    # Method 8: Chrome/Chromium headless
    print("\n8. Chrome headless...")
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        methods["Chrome Headless"] = True
        print("   SUCCESS: Available")
    except Exception as e:
        methods["Chrome Headless"] = False
        print("   ERROR: Not available")
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    working_methods = []
    for method, available in methods.items():
        status = "YES" if available else "NO"
        print(f"{method}: {status}")
        if available:
            working_methods.append(method)
    
    print(f"\nWorking methods: {len(working_methods)}/{len(methods)}")
    
    if working_methods:
        print("\nRECOMMENDED ORDER:")
        print("1. Python Libraries (pandas + reportlab) - Most reliable")
        print("2. Matplotlib - Good for tables")
        print("3. Microsoft Excel - Best formatting if available")
        print("4. LibreOffice - Free alternative to Excel")
        print("5. Chrome Headless - For HTML to PDF")
        print("6. WeasyPrint - HTML to PDF (requires setup)")
        print("7. pdfkit - HTML to PDF (requires wkhtmltopdf)")
    
    return working_methods

def test_python_libraries_method():
    """Test the Python libraries method with real data"""
    print("\n" + "="*60)
    print("TESTING PYTHON LIBRARIES METHOD")
    print("="*60)
    
    # Find Excel file
    downloads_dir = "downloads"
    if not os.path.exists(downloads_dir):
        print("ERROR: Downloads directory not found")
        return False
    
    excel_files = []
    for filename in os.listdir(downloads_dir):
        if filename.endswith(('.xlsx', '.xls')) and not filename.startswith('~$'):
            excel_files.append(filename)
    
    if not excel_files:
        print("ERROR: No Excel files found")
        return False
    
    latest_file = max(excel_files, key=lambda x: os.path.getctime(os.path.join(downloads_dir, x)))
    excel_path = os.path.join(downloads_dir, latest_file)
    
    print(f"Using Excel file: {latest_file}")
    
    try:
        import pandas as pd
        from reportlab.lib.pagesizes import letter, landscape
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
        from reportlab.lib import colors
        
        # Read Excel
        df = pd.read_excel(excel_path, sheet_name=0)
        print(f"Read {len(df)} rows, {len(df.columns)} columns")
        
        # Create PDF
        pdf_path = "test_python_method.pdf"
        doc = SimpleDocTemplate(pdf_path, pagesize=landscape(letter))
        
        # Convert to table
        table_data = [df.columns.tolist()] + df.values.tolist()
        table = Table(table_data)
        
        # Style the table
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
        ]))
        
        doc.build([table])
        
        if os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path)
            print(f"SUCCESS: PDF created - {file_size} bytes")
            print(f"File: {pdf_path}")
            return True
        else:
            print("ERROR: PDF not created")
            return False
            
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    working_methods = test_methods()
    
    if "Python Libraries" in working_methods:
        print("\n" + "="*60)
        print("RUNNING PRACTICAL TEST")
        print("="*60)
        test_python_libraries_method()
    else:
        print("\nNo working methods found!")
        print("You need to install at least one PDF conversion library.")

