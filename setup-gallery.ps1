param([string]$Root = "gallery")

Write-Host "`n=== Theophysics Gallery skeleton ==="
Write-Host "Current directory: $((Get-Location).Path)"
Write-Host "Target: '$Root'`n"

# Permission probe
try {
  "__probe__" | Out-File -FilePath ".\__write_probe__.tmp" -Encoding utf8 -ErrorAction Stop
  Remove-Item ".\__write_probe__.tmp" -ErrorAction SilentlyContinue
} catch {
  Write-Error "Cannot write in $((Get-Location).Path). Run PowerShell as Administrator or cd into a writable folder."
  exit 1
}

New-Item -ItemType Directory -Path "$Root","$Root\images","$Root\collections","$Root\descriptions" -Force | Out-Null

$index = @"
<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Theophysics Gallery</title></head>
<body>
<h1 style="font-family:system-ui">Theophysics Gallery Placeholder</h1>
<p>Replace with your real gallery HTML/CSS/JS.</p>
</body></html>
"@

if (!(Test-Path "$Root\index.html")) { $index | Out-File "$Root\index.html" -Encoding utf8 }
if (!(Test-Path "$Root\styles.css")) { "/* Your gallery CSS here */" | Out-File "$Root\styles.css" -Encoding utf8 }
if (!(Test-Path "$Root\app.js"))     { "// Your gallery JS here" | Out-File "$Root\app.js" -Encoding utf8 }
if (!(Test-Path "$Root\gallery.json"))     { "[]" | Out-File "$Root\gallery.json" -Encoding utf8 }
if (!(Test-Path "$Root\collections.json")) { "[]" | Out-File "$Root\collections.json" -Encoding utf8 }

Write-Host "`nCreated/verified folders & files under '$Root'."

# Auto-run build.py if present
if (Test-Path "$Root\build.py") {
  Write-Host "`nDetected build.py — attempting to run..."
  Push-Location $Root
  $py = (Get-Command py -ErrorAction SilentlyContinue) ?? (Get-Command python -ErrorAction SilentlyContinue)
  if ($py) { & $py.Source "build.py" } else { Write-Warning "Python not found. Run: python build.py" }
  Pop-Location
}

Write-Host "`n=== Done. Open '$Root\index.html'. ==="
