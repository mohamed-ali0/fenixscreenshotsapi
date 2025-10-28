import os
import subprocess
from datetime import datetime

def convert_excel_to_pdf_libreoffice(excel_path, pdf_path):
    """
    Convert Excel file to PDF using LibreOffice (no Excel required)
    """
    try:
        print(f"[{datetime.now()}] Converting Excel to PDF using LibreOffice...")
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
        
        # LibreOffice command for Excel to PDF conversion
        cmd = [
            'libreoffice',
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', os.path.dirname(pdf_path),
            '--infilter=calc8',
            excel_path
        ]
        
        print(f"[{datetime.now()}] Running command: {' '.join(cmd)}")
        
        # Run LibreOffice
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print(f"[{datetime.now()}] LibreOffice conversion successful")
            
            # Check if PDF was created
            if os.path.exists(pdf_path):
                print(f"[{datetime.now()}] PDF created: {pdf_path}")
                return True
            else:
                # Try to find the PDF with the same name as Excel
                excel_name = os.path.splitext(os.path.basename(excel_path))[0]
                expected_pdf = os.path.join(os.path.dirname(pdf_path), f"{excel_name}.pdf")
                
                if os.path.exists(expected_pdf):
                    # Rename to expected name
                    os.rename(expected_pdf, pdf_path)
                    print(f"[{datetime.now()}] PDF renamed to: {pdf_path}")
                    return True
                else:
                    print(f"[{datetime.now()}] PDF not found after conversion")
                    return False
        else:
            print(f"[{datetime.now()}] LibreOffice error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"[{datetime.now()}] LibreOffice conversion timed out")
        return False
    except FileNotFoundError:
        print(f"[{datetime.now()}] LibreOffice not found. Please install LibreOffice.")
        return False
    except Exception as e:
        print(f"[{datetime.now()}] Error in LibreOffice conversion: {str(e)}")
        return False

def convert_excel_to_pdf_python_libraries(excel_path, pdf_path):
    """
    Convert Excel to PDF using Python libraries (no Excel required)
    """
    try:
        print(f"[{datetime.now()}] Converting Excel to PDF using Python libraries...")
        
        import pandas as pd
        from reportlab.lib.pagesizes import letter, landscape
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
        from reportlab.lib import colors
        
        # Read Excel file
        df = pd.read_excel(excel_path, sheet_name=0)
        
        # Create PDF
        doc = SimpleDocTemplate(pdf_path, pagesize=landscape(letter))
        
        # Convert DataFrame to table data
        table_data = [df.columns.tolist()] + df.values.tolist()
        
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
        
        # Build PDF
        doc.build([table])
        
        print(f"[{datetime.now()}] Python library conversion successful: {pdf_path}")
        return True
        
    except ImportError as e:
        print(f"[{datetime.now()}] Missing Python library: {str(e)}")
        print(f"[{datetime.now()}] Install with: pip install pandas reportlab openpyxl")
        return False
    except Exception as e:
        print(f"[{datetime.now()}] Error in Python library conversion: {str(e)}")
        return False

def convert_excel_to_pdf_fallback(excel_path, pdf_path):
    """
    Fallback PDF conversion method (no Excel required)
    """
    print(f"[{datetime.now()}] Trying fallback PDF conversion methods...")
    
    # Try LibreOffice first
    if convert_excel_to_pdf_libreoffice(excel_path, pdf_path):
        return True
    
    # Try Python libraries
    if convert_excel_to_pdf_python_libraries(excel_path, pdf_path):
        return True
    
    print(f"[{datetime.now()}] All fallback methods failed")
    return False

if __name__ == "__main__":
    # Test the conversion
    excel_file = "downloads/2025-10-26_00-21-22.xlsx"
    pdf_file = "downloads/pdfs/2025-10-26_00-21-22.pdf"
    
    if os.path.exists(excel_file):
        convert_excel_to_pdf_fallback(excel_file, pdf_file)
    else:
        print(f"Excel file not found: {excel_file}")

