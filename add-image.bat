@echo off
setlocal ENABLEDELAYEDEXPANSION

REM Usage: add-image.bat <path-to-image> [root-folder]
set SRC=%~1
if "%SRC%"=="" (
  echo Usage: add-image.bat ^<path-to-image^> [root-folder]
  exit /b 1
)
if not exist "%SRC%" (
  echo File not found: %SRC%
  exit /b 1
)
set ROOT=%~2
if "%ROOT%"=="" set ROOT=gallery

set FN=%~nx1
set BASE=%~n1

REM Ensure folders
mkdir "%ROOT%\images" 2>nul
mkdir "%ROOT%\descriptions" 2>nul

REM Copy the image
copy /Y "%SRC%" "%ROOT%\images\%FN%" >nul

REM Create optional description sidecar (edit as needed)
if not exist "%ROOT%\descriptions\%BASE%.txt" (
  >"%ROOT%\descriptions\%BASE%.txt" echo Caption for %FN% (edit me).
)

echo Copied image to: %ROOT%\images\%FN%
echo Sidecar (caption) at: %ROOT%\descriptions\%BASE%.txt

REM Rebuild JSON if build.py exists
if exist "%ROOT%\build.py" (
  echo.
  echo Rebuilding gallery.json / collections.json...
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
