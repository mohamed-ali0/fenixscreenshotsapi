# Install PortOptimizer Screenshot API as Windows Service
# Run as Administrator

$projectPath = "C:\Users\Administrator\Downloads\portoptimizerbot"
$nssmPath = "C:\nssm\nssm.exe"

Write-Host "Installing PortOptimizer Screenshot API as Windows Service..."

# Check if NSSM exists
if (-not (Test-Path $nssmPath)) {
    Write-Host "ERROR: NSSM not found at $nssmPath"
    Write-Host "Please download NSSM from https://nssm.cc/download"
    Write-Host "Extract nssm.exe to C:\nssm\"
    exit 1
}

# Check if project directory exists
if (-not (Test-Path $projectPath)) {
    Write-Host "ERROR: Project directory not found at $projectPath"
    Write-Host "Please update the path in this script"
    exit 1
}

# Install service
Write-Host "Installing service..."
& $nssmPath install "PortOptimizerScreenshot" "$projectPath\start_service.bat"

# Configure service
Write-Host "Configuring service..."
& $nssmPath set "PortOptimizerScreenshot" AppDirectory $projectPath
& $nssmPath set "PortOptimizerScreenshot" Description "PortOptimizer Screenshot API Service"
& $nssmPath set "PortOptimizerScreenshot" Start SERVICE_AUTO_START
& $nssmPath set "PortOptimizerScreenshot" ObjectName LocalSystem
& $nssmPath set "PortOptimizerScreenshot" Type SERVICE_INTERACTIVE_PROCESS
& $nssmPath set "PortOptimizerScreenshot" AppExit Default Restart
& $nssmPath set "PortOptimizerScreenshot" AppRestartDelay 5000

# Start service
Write-Host "Starting service..."
& $nssmPath start "PortOptimizerScreenshot"

# Check status
Write-Host "Checking service status..."
& $nssmPath status "PortOptimizerScreenshot"

Write-Host ""
Write-Host "Service installation complete!"
Write-Host "Service name: PortOptimizerScreenshot"
Write-Host "Management commands:"
Write-Host "  Start:   net start PortOptimizerScreenshot"
Write-Host "  Stop:    net stop PortOptimizerScreenshot"
Write-Host "  Status:  sc query PortOptimizerScreenshot"
Write-Host ""
Write-Host "Test the API:"
Write-Host "  curl http://localhost:5000/status"
Write-Host ""


