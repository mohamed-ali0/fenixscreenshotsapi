"""
Install PDF conversion libraries
"""
import subprocess
import sys

def install_package(package):
    """Install a Python package"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False

def main():
    print("="*60)
    print("INSTALLING PDF CONVERSION LIBRARIES")
    print("="*60)
    
    # List of packages to install
    packages = [
        "reportlab",      # For PDF creation
        "matplotlib",     # For PDF creation via plots
        "weasyprint",     # For HTML to PDF conversion
    ]
    
    print("Installing PDF conversion libraries...")
    print("This will enable proper PDF conversion from Excel files.")
    print("="*60)
    
    success_count = 0
    for package in packages:
        print(f"\nInstalling {package}...")
        if install_package(package):
            success_count += 1
    
    print(f"\n{'='*60}")
    print(f"INSTALLATION COMPLETE")
    print(f"✅ Successfully installed: {success_count}/{len(packages)} packages")
    print("="*60)
    
    if success_count > 0:
        print("🎯 PDF conversion should now work!")
        print("Run the Excel processing test again to verify.")
    else:
        print("❌ No packages were installed successfully.")
        print("You may need to install them manually or check your Python environment.")

if __name__ == "__main__":
    main()

