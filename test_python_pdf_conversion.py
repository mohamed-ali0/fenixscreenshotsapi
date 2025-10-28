import os
import pandas as pd
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime

def test_python_pdf_conversion():
    """Test Python library PDF conversion"""
    print("=" * 60)
    print("TESTING PYTHON PDF CONVERSION")
    print("=" * 60)
    
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
    
    # Get the most recent file
    latest_file = max(excel_files, key=lambda x: os.path.getctime(os.path.join(downloads_dir, x)))
    excel_path = os.path.join(downloads_dir, latest_file)
    
    print(f"SUCCESS: Found Excel file: {latest_file}")
    
    # Create test output directory
    test_output_dir = "test_pdf_output"
    os.makedirs(test_output_dir, exist_ok=True)
    
    # Expected output path
    excel_name = os.path.splitext(os.path.basename(excel_path))[0]
    pdf_path = os.path.join(test_output_dir, f"{excel_name}_python.pdf")
    
    print(f"Input: {excel_path}")
    print(f"Output: {pdf_path}")
    
    try:
        print("\nReading Excel file...")
        # Read Excel file
        df = pd.read_excel(excel_path, sheet_name=0)
        print(f"SUCCESS: Read {len(df)} rows, {len(df.columns)} columns")
        
        # Show first few rows
        print("\nFirst 3 rows of data:")
        print(df.head(3).to_string())
        
        print("\nCreating PDF...")
        # Create PDF
        doc = SimpleDocTemplate(pdf_path, pagesize=landscape(letter))
        
        # Convert DataFrame to table data
        table_data = [df.columns.tolist()] + df.values.tolist()
        
        print(f"Table data: {len(table_data)} rows")
        
        # Create table
        table = Table(table_data)
        
        # Add table style
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        print("Building PDF...")
        # Build PDF
        doc.build([table])
        
        # Check if PDF was created
        if os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path)
            print(f"\nSUCCESS: PDF created successfully!")
            print(f"File: {pdf_path}")
            print(f"Size: {file_size} bytes")
            return True
        else:
            print("ERROR: PDF file not found after creation")
            return False
            
    except Exception as e:
        print(f"ERROR: Error during conversion: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_python_pdf_conversion()
    
    if success:
        print("\n" + "=" * 60)
        print("SUCCESS: Python PDF conversion works!")
        print("You can use this method instead of Excel COM automation.")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("FAILURE: Python PDF conversion failed")
        print("Check the error messages above.")
        print("=" * 60)

