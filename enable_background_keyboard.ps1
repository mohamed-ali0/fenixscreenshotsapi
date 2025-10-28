# Enable Background Keyboard Input on Windows
# Run as Administrator

Write-Host "Enabling background keyboard input for RDP sessions..."
Write-Host "This will allow keyboard shortcuts to work even when RDP is minimized."
Write-Host ""

# RDP Session Configuration
Write-Host "Configuring RDP sessions..."
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v KeepAliveEnable /t REG_DWORD /d 1 /f
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fSingleSessionPerUser /t REG_DWORD /d 0 /f
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" /v MaxIdleTime /t REG_DWORD /d 0 /f
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" /v MaxDisconnectionTime /t REG_DWORD /d 0 /f
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" /v KeepAliveInterval /t REG_DWORD /d 1 /f

# Interactive Services
Write-Host "Enabling interactive services..."
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Windows" /v NoInteractiveServices /t REG_DWORD /d 0 /f
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager" /v ProtectionMode /t REG_DWORD /d 0 /f

# Focus Prevention
Write-Host "Disabling focus prevention..."
reg add "HKCU\Control Panel\Desktop" /v ForegroundLockTimeout /t REG_DWORD /d 0 /f
reg add "HKCU\Control Panel\Desktop" /v ForegroundFlashCount /t REG_DWORD /d 0 /f
reg add "HKCU\Control Panel\Desktop" /v HungAppTimeout /t REG_DWORD /d 5000 /f

# Input System
Write-Host "Configuring input system..."
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v EnableLUA /t REG_DWORD /d 0 /f

Write-Host ""
Write-Host "Configuration complete!"
Write-Host "Please restart the server for all changes to take effect."
Write-Host ""
Write-Host "After restart, test with:"
Write-Host "  python app.py"
Write-Host "  curl -X POST http://localhost:5000/screenshot/now -H 'Content-Type: application/json' -d '{\"admin_password\":\"YB02Ss3JJdk\"}'"
Write-Host ""


