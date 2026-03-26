@echo off
setlocal

where python >nul 2>nul
if %errorlevel% neq 0 (
  echo Python was not found in PATH.
  pause
  exit /b 1
)

python mega_autopromo_generator.py
if %errorlevel% neq 0 (
  echo.
  echo Failed to start Mega AutoPromo Generator.
  pause
  exit /b %errorlevel%
)

endlocal
