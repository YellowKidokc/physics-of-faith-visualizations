#!/usr/bin/env python3
"""
THEOPHYSICS Auto-Gallery Updater with Custom Descriptions
Automatically scans folders and updates gallery with new visualizations
Supports custom descriptions via .txt or .md files
"""

import os
import json
import time
import shutil
from pathlib import Path

# Configuration
SOURCE_FOLDERS = {
    'html': r'C:\Users\Yellowkid\Desktop\theophysics-website',
    'svg': r'C:\Users\Yellowkid\Desktop\PICS',
    'descriptions': r'C:\Users\Yellowkid\Desktop\descriptions'  # New folder for description files
}

GALLERY_PATH = r'C:\Users\Yellowkid\Desktop\theophysics-website'

def ensure_description_folder():
    """Create descriptions folder if it doesn't exist"""
    desc_folder = Path(SOURCE_FOLDERS['descriptions'])
    if not desc_folder.exists():
        desc_folder.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created descriptions folder: {desc_folder}")
        
        # Create example description files
        examples = {
            'master-equation-final.txt': 'The Master Equation visualization showing the complete unified framework that mathematically describes the salvation narrative through 10 integrated variables representing physical and spiritual reality.',
            'quantum-trinity-spiral.md': '''# Quantum Trinity Spiral
            
**Revolutionary visualization** combining:
- Trinity doctrine with quantum field theory
- Three-person unity through quantum entanglement
- Mathematical proof of divine relationship structure

*This unique model demonstrates how the Trinity operates as a perfect quantum system with infinite binding energy.*''',
            'consciousness-gravity-comparison.txt': 'Side-by-side comparison showing how consciousness follows the same mathematical principles as gravitational fields, demonstrating the deep structural unity between mind and matter.'
        }
        
        for filename, content in examples.items():
            example_file = desc_folder / filename
            with open(example_file, 'w', encoding='utf-8') as f:
                f.write(content)
        
        print(f"📝 Created {len(examples)} example description files")

def load_custom_description(filename):
    """Load custom description from .txt or .md file"""
    base_name = Path(filename).stem
    desc_folder = Path(SOURCE_FOLDERS['descriptions'])
    
    # Try .md first, then .txt
    for ext in ['.md', '.txt']:
        desc_file = desc_folder / f"{base_name}{ext}"
        if desc_file.exists():
            try:
                content = desc_file.read_text(encoding='utf-8')
                print(f"📖 Loaded custom description: {desc_file.name}")
                return content.strip()
            except Exception as e:
                print(f"❌ Error reading {desc_file}: {e}")
    
    return None

def generate_default_description(filename):
    """Generate smart default descriptions based on filename"""
    descriptions = {
        # Quantum
        'quantum': 'Explores quantum mechanical principles applied to spiritual reality and consciousness, demonstrating the mathematical unity between physical and theological frameworks.',
        'entanglement': 'Visualizes the non-local connections between spiritual entities, showing how quantum entanglement provides a scientific model for divine relationships.',
        'consciousness': 'Maps the relationship between consciousness and physical reality through quantum information theory and observer effects.',
        'trinity': 'Mathematical representation of Trinitarian relationships using quantum field theory and advanced physics principles.',
        
        # Master Equation
        'master-equation': 'Components and interactions within the unified Master Equation framework that mathematically describes the complete salvation narrative.',
        'unified': 'Integration of multiple theoretical frameworks into cohesive models showing the deep structure underlying both physics and theology.',
        
        # Entropy/Grace
        'entropy': 'The interplay between spiritual decay and divine ordering principles, demonstrating grace as negentropy in spiritual thermodynamics.',
        'grace': 'Mathematical modeling of divine grace as negentropy in spiritual systems, showing how God\'s intervention reverses spiritual decay.',
        'sin': 'Thermodynamic analysis of sin as spiritual entropy, providing a scientific framework for understanding moral corruption.',
        
        # Forces  
        'gravity': 'Parallels between gravitational and spiritual attractive forces, showing how sin creates spiritual gravity wells requiring divine escape velocity.',
        'strong-force': 'Nuclear binding forces as models for divine unity, demonstrating how covenant relationships mirror the strongest force in physics.',
        'electromagnetic': 'Light and truth as electromagnetic phenomena, revealing how divine revelation operates through the same principles as physical light.',
        
        # Spiritual Physics
        'spiritual': 'Direct applications of physical laws to spiritual realities, demonstrating the mathematical foundations underlying theological truths.',
        'faith': 'Network theory and field dynamics applied to faith communities, showing how spiritual authority and relationships follow physical principles.',
        'light': 'Truth as electromagnetic radiation in spiritual spectra, demonstrating how divine illumination follows the same laws as physical light.'
    }
    
    filename_lower = filename.lower()
    for key, desc in descriptions.items():
        if key in filename_lower:
            return desc
    
    return 'Advanced visualization integrating physics and theology through mathematical frameworks, demonstrating the deep unity between scientific and spiritual truth.'

def scan_files():
    """Scan source folders for HTML and SVG files"""
    files = {
        'html': [],
        'svg': []
    }
    
    # Scan HTML files
    html_folder = Path(SOURCE_FOLDERS['html'])
    if html_folder.exists():
        for file in html_folder.glob('*.html'):
            if file.name != 'index.html':  # Skip the gallery itself
                # Load custom description or generate default
                custom_desc = load_custom_description(file.name)
                description = custom_desc if custom_desc else generate_default_description(file.name)
                
                files['html'].append({
                    'name': file.stem.replace('-', ' ').title(),
                    'filename': file.name,
                    'path': str(file),
                    'size': file.stat().st_size,
                    'modified': file.stat().st_mtime,
                    'description': description,
                    'has_custom_desc': custom_desc is not None
                })
    
    # Scan SVG files
    svg_folder = Path(SOURCE_FOLDERS['svg'])
    if svg_folder.exists():
        for file in svg_folder.glob('*.svg'):
            # Load custom description or generate default
            custom_desc = load_custom_description(file.name)
            description = custom_desc if custom_desc else generate_default_description(file.name)
            
            files['svg'].append({
                'name': file.stem.replace('-', ' ').title(),
                'filename': file.name,
                'path': str(file),
                'size': file.stat().st_size,
                'modified': file.stat().st_mtime,
                'description': description,
                'has_custom_desc': custom_desc is not None
            })
    
    return files

def copy_svg_files():
    """Copy SVG files to website images folder"""
    svg_folder = Path(SOURCE_FOLDERS['svg'])
    target_folder = Path(GALLERY_PATH) / 'images'
    
    if not target_folder.exists():
        target_folder.mkdir(exist_ok=True)
    
    copied_count = 0
    for svg_file in svg_folder.glob('*.svg'):
        target_file = target_folder / svg_file.name
        if not target_file.exists() or svg_file.stat().st_mtime > target_file.stat().st_mtime:
            shutil.copy2(svg_file, target_file)
            copied_count += 1
    
    if copied_count > 0:
        print(f"📁 Copied {copied_count} SVG files to images folder")

def copy_description_files():
    """Copy description files to website descriptions folder"""
    desc_folder = Path(SOURCE_FOLDERS['descriptions'])
    target_folder = Path(GALLERY_PATH) / 'descriptions'
    
    if not desc_folder.exists():
        return
        
    if not target_folder.exists():
        target_folder.mkdir(exist_ok=True)
    
    copied_count = 0
    for desc_file in desc_folder.glob('*'):
        if desc_file.suffix in ['.txt', '.md']:
            target_file = target_folder / desc_file.name
            if not target_file.exists() or desc_file.stat().st_mtime > target_file.stat().st_mtime:
                shutil.copy2(desc_file, target_file)
                copied_count += 1
    
    if copied_count > 0:
        print(f"📝 Copied {copied_count} description files")

def generate_gallery_data(files):
    """Generate JavaScript data for the gallery"""
    custom_count = sum(1 for f in files['html'] + files['svg'] if f['has_custom_desc'])
    
    js_data = f"""
// Auto-generated gallery data - {time.strftime('%Y-%m-%d %H:%M:%S')}
const galleryData = {json.dumps(files, indent=2)};

// Update gallery stats
document.getElementById('total-count').textContent = {len(files['html']) + len(files['svg'])};
document.getElementById('completed-count').textContent = {len(files['html']) + len(files['svg']) - 5};

console.log('Gallery updated with {len(files['html'])} HTML and {len(files['svg'])} SVG files');
console.log('Custom descriptions: {custom_count}/{len(files['html']) + len(files['svg'])}');
"""
    return js_data

def update_gallery():
    """Update the gallery with latest file data"""
    print("🔄 Scanning for new visualizations...")
    
    # Ensure folders exist
    ensure_description_folder()
    
    # Copy files
    copy_svg_files()
    copy_description_files()
    
    # Scan files
    files = scan_files()
    custom_count = sum(1 for f in files['html'] + files['svg'] if f['has_custom_desc'])
    
    print(f"📊 Found {len(files['html'])} HTML files and {len(files['svg'])} SVG files")
    print(f"📝 Custom descriptions: {custom_count}/{len(files['html']) + len(files['svg'])}")
    
    # Generate gallery data
    js_data = generate_gallery_data(files)
    
    # Write to gallery data file
    gallery_data_path = Path(GALLERY_PATH) / 'gallery-data.js'
    with open(gallery_data_path, 'w', encoding='utf-8') as f:
        f.write(js_data)
    
    print(f"✅ Gallery data updated: {gallery_data_path}")
    
    return files

def main():
    """Main update loop"""
    print("🚀 THEOPHYSICS Auto-Gallery Updater Started")
    print("=" * 50)
    print("📁 Monitoring folders:")
    print(f"   HTML: {SOURCE_FOLDERS['html']}")
    print(f"   SVG:  {SOURCE_FOLDERS['svg']}")
    print(f"   DESC: {SOURCE_FOLDERS['descriptions']}")
    print("\n💡 To add custom descriptions:")
    print("   1. Create filename.txt or filename.md in descriptions folder")
    print("   2. Use same base name as your visualization")
    print("   3. Example: master-equation-final.txt for master-equation-final.svg")
    print("=" * 50)
    
    while True:
        try:
            files = update_gallery()
            print(f"⏰ Next scan in 30 seconds... ({time.strftime('%H:%M:%S')})")
            time.sleep(30)
        except KeyboardInterrupt:
            print("\n👋 Gallery updater stopped")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()
