@echo off
setlocal ENABLEDELAYEDEXPANSION

REM Usage: new-collection.bat <slug> [root-folder]
set SLUG=%~1
if "%SLUG%"=="" (
  echo Usage: new-collection.bat ^<slug^> [root-folder]
  echo   Example: new-collection.bat master-equation gallery
  exit /b 1
)
set ROOT=%~2
if "%ROOT%"=="" set ROOT=gallery

set COLDIR=%ROOT%\collections\%SLUG%
mkdir "%COLDIR%" 2>nul

REM Minimal index.html (you can overwrite with your full set later)
>"%COLDIR%\index.html" echo ^<!DOCTYPE html^>
>>"%COLDIR%\index.html" echo ^<html lang="en"^>^<head^>^<meta charset="utf-8"^>^<meta name="viewport" content="width=device-width,initial-scale=1"^>^<title>%SLUG% — Collection^</title^>^</head^>^<body^>
>>"%COLDIR%\index.html" echo ^<h1 style="font-family:system-ui">%SLUG% (Collection Placeholder)^</h1^>
>>"%COLDIR%\index.html" echo ^<p>Add your multi-page set here. This folder is now featured.^</p^>
>>"%COLDIR%\index.html" echo ^</body^>^</html^>

REM Optional meta.json scaffold
if not exist "%COLDIR%\meta.json" (
  >"%COLDIR%\meta.json" echo {
  >>"%COLDIR%\meta.json" echo   "summary": "High-quality multi-page set.",
  >>"%COLDIR%\meta.json" echo   "tags": ["IMPORTANT","set"],
  >>"%COLDIR%\meta.json" echo   "cover": "collections/%SLUG%/cover.jpg"
  >>"%COLDIR%\meta.json" echo }
)

echo Created collection folder:
echo   %COLDIR%
echo   %COLDIR%\index.html
echo   %COLDIR%\meta.json

REM Rebuild JSON if build.py exists
if exist "%ROOT%\build.py" (
  echo.
  echo Rebuilding collections.json / gallery.json...
  pushd "%ROOT%"
  where py >nul 2>nul
  if %ERRORLEVEL%==0 ( py -3 build.py ) else (
    where python >nul 2>nul
    if %ERRORLEVEL%==0 ( python build.py ) else ( echo Python not found; run build manually. )
  )
  popd
)

echo Done. Open "%ROOT%\index.html".
endlocal
