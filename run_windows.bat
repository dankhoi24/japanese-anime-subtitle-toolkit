@echo off
cd /d "%~dp0"
py -3 scripts\build.py --start 1 --end 10
if errorlevel 1 (
  echo Build failed. See README.md for manual source instructions.
  pause
  exit /b 1
)
py -3 scripts\validate.py output\chis-sweet-home
pause
