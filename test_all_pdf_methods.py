import os
import subprocess
import sys
from datetime import datetime

def test_method_1_python_libraries():
    """Test Python libraries (pandas + reportlab)"""
    print("\n" + "="*50)
    print("METHOD 1: Python Libraries (pandas + reportlab)")
    print("="*50)
    
    try:
        import pandas as pd
        from reportlab.lib.pagesizes import letter, landscape
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
        from reportlab.lib import colors
        
        print("SUCCESS: All required libraries available")
        
        # Test with sample data
        df = pd.DataFrame({
            'Date': ['2025-10-26', '2025-10-27'],
            'Container': ['20ST', '40HC'],
            'Status': ['YES', 'NO']
        })
        
        pdf_path = "test_output_method1.pdf"
        doc = SimpleDocTemplate(pdf_path, pagesize=landscape(letter))
        table_data = [df.columns.tolist()] + df.values.tolist()
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey)
        ]))
        doc.build([table])
        
        if os.path.exists(pdf_path):
            print(f"SUCCESS: PDF created - {os.path.getsize(pdf_path)} bytes")
            os.remove(pdf_path)
            return True
        else:
            print("ERROR: PDF not created")
            return False
            
    except ImportError as e:
        print(f"ERROR: Missing library - {e}")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_method_2_weasyprint():
    """Test WeasyPrint (HTML to PDF)"""
    print("\n" + "="*50)
    print("METHOD 2: WeasyPrint (HTML to PDF)")
    print("="*50)
    
    try:
        import weasyprint
        import pandas as pd
        
        print("SUCCESS: WeasyPrint available")
        
        # Create HTML from Excel data
        df = pd.DataFrame({
            'Date': ['2025-10-26', '2025-10-27'],
            'Container': ['20ST', '40HC'],
            'Status': ['YES', 'NO']
        })
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid black; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                @page {{ size: A4 landscape; }}
            </style>
        </head>
        <body>
            <h1>Port Optimizer Report</h1>
            {df.to_html(index=False, classes='table')}
        </body>
        </html>
        """
        
        pdf_path = "test_output_method2.pdf"
        weasyprint.HTML(string=html_content).write_pdf(pdf_path)
        
        if os.path.exists(pdf_path):
            print(f"SUCCESS: PDF created - {os.path.getsize(pdf_path)} bytes")
            os.remove(pdf_path)
            return True
        else:
            print("ERROR: PDF not created")
            return False
            
    except ImportError as e:
        print(f"ERROR: WeasyPrint not installed - {e}")
        print("Install with: pip install weasyprint")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_method_3_matplotlib():
    """Test Matplotlib (plot to PDF)"""
    print("\n" + "="*50)
    print("METHOD 3: Matplotlib (plot to PDF)")
    print("="*50)
    
    try:
        import matplotlib.pyplot as plt
        import pandas as pd
        from matplotlib.backends.backend_pdf import PdfPages
        
        print("SUCCESS: Matplotlib available")
        
        # Create sample data
        df = pd.DataFrame({
            'Date': ['2025-10-26', '2025-10-27', '2025-10-28'],
            'Container': ['20ST', '40HC', '40ST'],
            'Status': ['YES', 'NO', 'YES']
        })
        
        pdf_path = "test_output_method3.pdf"
        
        with PdfPages(pdf_path) as pdf:
            fig, ax = plt.subplots(figsize=(11, 8.5))  # Legal size
            ax.axis('tight')
            ax.axis('off')
            
            # Create table
            table_data = [df.columns.tolist()] + df.values.tolist()
            table = ax.table(cellText=table_data[1:], colLabels=table_data[0], 
                           cellLoc='center', loc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.scale(1.2, 1.5)
            
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()
        
        if os.path.exists(pdf_path):
            print(f"SUCCESS: PDF created - {os.path.getsize(pdf_path)} bytes")
            os.remove(pdf_path)
            return True
        else:
            print("ERROR: PDF not created")
            return False
            
    except ImportError as e:
        print(f"ERROR: Matplotlib not installed - {e}")
        print("Install with: pip install matplotlib")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_method_4_pdfkit():
    """Test pdfkit (wkhtmltopdf wrapper)"""
    print("\n" + "="*50)
    print("METHOD 4: pdfkit (wkhtmltopdf wrapper)")
    print("="*50)
    
    try:
        import pdfkit
        import pandas as pd
        
        print("SUCCESS: pdfkit available")
        
        # Check if wkhtmltopdf is installed
        try:
            pdfkit.configuration()
            print("SUCCESS: wkhtmltopdf binary found")
        except:
            print("ERROR: wkhtmltopdf binary not found")
            print("Download from: https://wkhtmltopdf.org/downloads.html")
            return False
        
        # Create HTML
        df = pd.DataFrame({
            'Date': ['2025-10-26', '2025-10-27'],
            'Container': ['20ST', '40HC'],
            'Status': ['YES', 'NO']
        })
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid black; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                @page {{ size: A4 landscape; }}
            </style>
        </head>
        <body>
            <h1>Port Optimizer Report</h1>
            {df.to_html(index=False, classes='table')}
        </body>
        </html>
        """
        
        pdf_path = "test_output_method4.pdf"
        options = {
            'page-size': 'A4',
            'orientation': 'Landscape',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in'
        }
        
        pdfkit.from_string(html_content, pdf_path, options=options)
        
        if os.path.exists(pdf_path):
            print(f"SUCCESS: PDF created - {os.path.getsize(pdf_path)} bytes")
            os.remove(pdf_path)
            return True
        else:
            print("ERROR: PDF not created")
            return False
            
    except ImportError as e:
        print(f"ERROR: pdfkit not installed - {e}")
        print("Install with: pip install pdfkit")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_method_5_pywin32_print():
    """Test Windows Print to PDF (pywin32)"""
    print("\n" + "="*50)
    print("METHOD 5: Windows Print to PDF (pywin32)")
    print("="*50)
    
    try:
        import win32com.client
        import pandas as pd
        
        print("SUCCESS: pywin32 available")
        
        # Create Excel file
        df = pd.DataFrame({
            'Date': ['2025-10-26', '2025-10-27'],
            'Container': ['20ST', '40HC'],
            'Status': ['YES', 'NO']
        })
        
        excel_path = "test_data.xlsx"
        df.to_excel(excel_path, index=False)
        
        # Use Excel COM to print to PDF
        excel = win32com.client.Dispatch("Excel.Application")
        excel.Visible = False
        excel.DisplayAlerts = False
        
        workbook = excel.Workbooks.Open(os.path.abspath(excel_path))
        worksheet = workbook.Worksheets.Item(1)
        
        # Set page setup
        worksheet.PageSetup.Orientation = 2  # xlLandscape
        worksheet.PageSetup.PaperSize = 5    # xlPaperLegal
        
        # Print to PDF
        pdf_path = "test_output_method5.pdf"
        worksheet.PrintOut(PrintToFile=True, PrToFileName=os.path.abspath(pdf_path))
        
        workbook.Close()
        excel.Quit()
        
        if os.path.exists(pdf_path):
            print(f"SUCCESS: PDF created - {os.path.getsize(pdf_path)} bytes")
            os.remove(pdf_path)
            os.remove(excel_path)
            return True
        else:
            print("ERROR: PDF not created")
            os.remove(excel_path)
            return False
            
    except ImportError as e:
        print(f"ERROR: pywin32 not installed - {e}")
        print("Install with: pip install pywin32")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_method_6_powershell_print():
    """Test PowerShell Print to PDF"""
    print("\n" + "="*50)
    print("METHOD 6: PowerShell Print to PDF")
    print("="*50)
    
    try:
        import pandas as pd
        
        # Create Excel file
        df = pd.DataFrame({
            'Date': ['2025-10-26', '2025-10-27'],
            'Container': ['20ST', '40HC'],
            'Status': ['YES', 'NO']
        })
        
        excel_path = "test_data.xlsx"
        df.to_excel(excel_path, index=False)
        
        # PowerShell script to print to PDF
        ps_script = f'''
        $excel = New-Object -ComObject Excel.Application
        $excel.Visible = $false
        $excel.DisplayAlerts = $false
        
        try {{
            $workbook = $excel.Workbooks.Open('{os.path.abspath(excel_path)}')
            $worksheet = $workbook.Worksheets.Item(1)
            
            # Set to Legal landscape
            $worksheet.PageSetup.Orientation = 2
            $worksheet.PageSetup.PaperSize = 5
            
            # Print to PDF
            $pdf_path = '{os.path.abspath("test_output_method6.pdf")}'
            $worksheet.PrintOut(PrintToFile=$true, PrToFileName=$pdf_path)
            
            $workbook.Close()
            $excel.Quit()
            
            Write-Host "PDF created: $pdf_path"
        }} catch {{
            Write-Host "Error: $_"
            $excel.Quit()
        }}
        '''
        
        with open('temp_print.ps1', 'w') as f:
            f.write(ps_script)
        
        result = subprocess.run(['powershell', '-ExecutionPolicy', 'Bypass', '-File', 'temp_print.ps1'], 
                              capture_output=True, text=True, timeout=30)
        
        # Cleanup
        os.remove('temp_print.ps1')
        os.remove(excel_path)
        
        if result.returncode == 0 and os.path.exists("test_output_method6.pdf"):
            file_size = os.path.getsize("test_output_method6.pdf")
            print(f"SUCCESS: PDF created - {file_size} bytes")
            os.remove("test_output_method6.pdf")
            return True
        else:
            print(f"ERROR: PowerShell failed - {result.stderr}")
            return False
            
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    print("="*60)
    print("TESTING ALL PDF CONVERSION METHODS")
    print("="*60)
    
    methods = [
        ("Python Libraries (pandas + reportlab)", test_method_1_python_libraries),
        ("WeasyPrint (HTML to PDF)", test_method_2_weasyprint),
        ("Matplotlib (plot to PDF)", test_method_3_matplotlib),
        ("pdfkit (wkhtmltopdf)", test_method_4_pdfkit),
        ("Windows Print to PDF (pywin32)", test_method_5_pywin32_print),
        ("PowerShell Print to PDF", test_method_6_powershell_print)
    ]
    
    results = {}
    
    for name, test_func in methods:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"ERROR: {name} crashed - {e}")
            results[name] = False
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY OF AVAILABLE METHODS")
    print("="*60)
    
    working_methods = []
    for name, success in results.items():
        status = "✅ WORKS" if success else "❌ FAILED"
        print(f"{name}: {status}")
        if success:
            working_methods.append(name)
    
    print(f"\nWorking methods: {len(working_methods)}/{len(methods)}")
    
    if working_methods:
        print("\nRECOMMENDED ORDER OF PREFERENCE:")
        for i, method in enumerate(working_methods, 1):
            print(f"{i}. {method}")
    else:
        print("\n❌ NO WORKING METHODS FOUND!")
        print("You may need to install additional software.")

if __name__ == "__main__":
    main()

