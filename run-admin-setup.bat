@echo off
:: Relaunch this script as admin if not elevated
net session >nul 2>&1
if %errorlevel% NEQ 0 (
  powershell -NoProfile -Command "Start-Process -Verb RunAs -FilePath '%~f0'"
  exit /b
)

call setup-gallery.bat gallery
