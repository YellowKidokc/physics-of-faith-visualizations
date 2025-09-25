@echo off
setlocal ENABLEDELAYEDEXPANSION

REM Usage: setup-gallery.bat [target-folder]
set "ROOT=%~1"
if "%ROOT%"=="" set "ROOT=gallery"

echo.
echo === Theophysics Gallery skeleton ===
echo Current directory: %CD%
echo Target: "%ROOT%"
echo.

REM 1) Permission probe (try to write a temp file in current directory)
set "_probe=%CD%\__write_probe__.tmp"
echo test > "%_probe%" 2>&1
if not exist "%_probe%" (
  echo [ERROR] Cannot write in "%CD%".
  echo Try: Right-click this .bat and "Run as administrator" OR cd into a writable folder (Documents/Repos).
  echo Aborting.
  exit /b 1
) else (
  del "%_probe%" >nul 2>&1
)

REM 2) Create directories (NO error-hiding)
mkdir "%ROOT%"
mkdir "%ROOT%\images"
mkdir "%ROOT%\collections"
mkdir "%ROOT%\descriptions"

REM 3) Create placeholder files if missing
if not exist "%ROOT%\index.html" (
  >"%ROOT%\index.html" echo ^<!DOCTYPE html^>
  >>"%ROOT%\index.html" echo ^<html lang="en"^>^<head^>^<meta charset="utf-8"^>^<meta name="viewport" content="width=device-width,initial-scale=1"^>^<title>Theophysics Gallery^</title^>^</head^>^<body^>
  >>"%ROOT%\index.html" echo ^<h1 style="font-family:system-ui">Theophysics Gallery Placeholder^</h1^>
  >>"%ROOT%\index.html" echo ^<p>Replace with your real gallery HTML/CSS/JS.^</p^>
  >>"%ROOT%\index.html" echo ^</body^>^</html^>
)

if not exist "%ROOT%\styles.css"  ( echo /* Your gallery CSS here */>"%ROOT%\styles.css" )
if not exist "%ROOT%\app.js"      ( echo // Your gallery JS here >"%ROOT%\app.js" )
if not exist "%ROOT%\gallery.json"     ( echo []>"%ROOT%\gallery.json" )
if not exist "%ROOT%\collections.json" ( echo []>"%ROOT%\collections.json" )

echo.
echo Created/verified:
echo   %ROOT%\
echo   %ROOT%\images\
echo   %ROOT%\collections\
echo   %ROOT%\descriptions\
echo   %ROOT%\index.html (placeholder)
echo   %ROOT%\styles.css (placeholder)
echo   %ROOT%\app.js     (placeholder)
echo   %ROOT%\gallery.json (empty)
echo   %ROOT%\collections.json (empty)

REM 4) Auto-run build.py if present
if exist "%ROOT%\build.py" (
  echo.
  echo Detected build.py — attempting to run...
  pushd "%ROOT%"
  where py >nul 2>&1
  if %ERRORLEVEL%==0 (
    py -3 build.py
  ) else (
    where python >nul 2>&1
    if %ERRORLEVEL%==0 (
      python build.py
    ) else (
      echo [WARN] Python not found. Run manually later:
      echo   cd "%ROOT%" ^&^& python build.py
    )
  )
  popd
)

echo.
echo === Done. Open "%ROOT%\index.html". ===
endlocal
