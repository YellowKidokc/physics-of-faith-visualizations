# Setup Collections - PowerShell Script for Cloudflare Gallery
# This creates the proper folder structure for featured collections

Write-Host "Setting up Cloudflare Gallery Collections..." -ForegroundColor Cyan

# Ensure collections folder exists
New-Item -ItemType Directory -Path "collections" -Force | Out-Null

# Create unavoidable-conclusion collection
$collectionPath = "collections\unavoidable-conclusion"
New-Item -ItemType Directory -Path $collectionPath -Force | Out-Null

# Copy the unavoidable conclusion HTML from the document you showed me
$unavoidableHTML = @"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Unavoidable Conclusion: A Proof of God from First Principles</title>
    <style>
        /* Add minimal styles for the collection version */
        body { font-family: Georgia, serif; background: #0f0f0f; color: #f8f9fa; }
        .nav { position: fixed; top: 0; background: rgba(26,26,26,0.95); padding: 1rem; width: 100%; z-index: 1000; }
        .nav a { color: #D4AF37; text-decoration: none; font-weight: bold; }
        .container { margin-top: 80px; padding: 2rem; max-width: 1000px; margin-left: auto; margin-right: auto; }
        .hero { text-align: center; padding: 4rem 0; background: linear-gradient(135deg, #D4AF37, #2E86AB); margin: -2rem -2rem 3rem -2rem; }
        .hero h1 { font-size: 3rem; margin-bottom: 1rem; color: #0f0f0f; }
        .hero p { font-size: 1.2rem; color: #0f0f0f; }
        .gates-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; margin: 3rem 0; }
        .gate { background: rgba(255,255,255,0.05); padding: 2rem; border-radius: 15px; border: 2px solid #D4AF37; }
        .gate h3 { color: #D4AF37; margin-bottom: 1rem; }
    </style>
</head>
<body>
    <nav class="nav">
        <a href="../../index.html">← Back to Gallery</a>
    </nav>
    <div class="container">
        <div class="hero">
            <h1>The Unavoidable Conclusion</h1>
            <p>A Proof of God from First Principles</p>
        </div>
        
        <div class="gates-grid">
            <div class="gate">
                <h3>Gate 1: Duality</h3>
                <p>Do you see the difference between building and breaking? This simple question unlocks the fundamental structure of reality.</p>
            </div>
            <div class="gate">
                <h3>Gate 2: Nature</h3>
                <p>Can pure creativity create pure destruction? The answer reveals the asymmetry at the heart of existence.</p>
            </div>
            <div class="gate">
                <h3>Gate 3: Shadow</h3>
                <p>What do shadows tell us about light? The final piece of the logical puzzle falls into place.</p>
            </div>
        </div>
        
        <div style="background: rgba(255,215,0,0.1); padding: 2rem; border-radius: 15px; margin: 3rem 0;">
            <h2 style="color: #D4AF37; text-align: center;">The Complete Logical Proof</h2>
            <p>Through three simple questions about reality itself, we arrive at an unavoidable conclusion: the existence of evil proves the existence of a purely good Creator, and identifies the source of shadows in our world.</p>
        </div>
    </div>
</body>
</html>
"@

$unavoidableHTML | Out-File -FilePath "$collectionPath\index.html" -Encoding UTF8

# Create meta.json for unavoidable-conclusion
$metaJson = @"
{
  "summary": "A complete logical proof of God's existence using only reason and three simple questions about reality. No faith required - just logic.",
  "tags": ["FEATURED", "logic", "proof", "philosophy", "three-gates"],
  "cover": "images/master-equation-final.svg",
  "pages": 1,
  "images": 0
}
"@

$metaJson | Out-File -FilePath "$collectionPath\meta.json" -Encoding UTF8

# Create physics-of-faith collection  
$physicsPath = "collections\physics-of-faith"
New-Item -ItemType Directory -Path $physicsPath -Force | Out-Null

# Copy your existing physics-of-faith.html (simplified version)
Copy-Item "physics-of-faith.html" "$physicsPath\index.html" -Force

# Create meta.json for physics-of-faith
$physicsMetaJson = @"
{
  "summary": "Interactive visualization showing how 12 theoretical frameworks all converge on Jesus Christ as the unified center of reality through the Logos principle.",
  "tags": ["FEATURED", "interactive", "12-theories", "logos", "convergence"],
  "cover": "images/christ-unification-principle.svg",
  "pages": 1,
  "images": 1
}
"@

$physicsMetaJson | Out-File -FilePath "$physicsPath\meta.json" -Encoding UTF8

Write-Host "Collections created successfully!" -ForegroundColor Green
Write-Host "- unavoidable-conclusion (logical proof)" -ForegroundColor Yellow
Write-Host "- physics-of-faith (12 theories convergence)" -ForegroundColor Yellow

# Run build.py if it exists
if (Test-Path "build.py") {
    Write-Host "`nRunning build.py to update gallery..." -ForegroundColor Cyan
    $python = (Get-Command py -ErrorAction SilentlyContinue) ?? (Get-Command python -ErrorAction SilentlyContinue)
    if ($python) {
        & $python.Source "build.py"
        Write-Host "Gallery updated!" -ForegroundColor Green
    } else {
        Write-Warning "Python not found. Run manually: python build.py"
    }
} else {
    Write-Warning "build.py not found in current directory"
}

Write-Host "`nDone! Open index.html to see your featured collections at the top!" -ForegroundColor Green
