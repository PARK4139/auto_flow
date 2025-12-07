@echo off
setlocal enabledelayedexpansion

set SUBNET=172.21.239

echo Scanning %SUBNET%.1-254 for SSH (port 22)...
echo.

for /L %%i in (1,1,254) do (
    set IP=%SUBNET%.%%i
    powershell -command "if (Test-NetConnection -ComputerName !IP! -Port 22 -InformationLevel Quiet) {Write-Output '✅ SSH open: !IP!'}"
)

echo.
echo Scan complete.
pause
