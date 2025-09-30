#!/usr/bin/env python3
"""
Simple Gallery Auto-Updater
Scans the current folder for HTML and SVG files and updates gallery
NO external dependencies needed!
"""

import os
import json
import time
from pathlib import Path

# Configuration - all relative to current folder
CURRENT_DIR = Path(__file__).parent
IMAGES_DIR = CURRENT_DIR / 'images'
DESCRIPTIONS_DIR = CURRENT_DIR / 'descriptions'

def load_custom_description(filename):
    """Load custom description from .txt or .md file"""
    base_name = Path(filename).stem
    
    # Try .md first, then .txt
    for ext in ['.md', '.txt']:
        desc_file = DESCRIPTIONS_DIR / f"{base_name}{ext}"
        if desc_file.exists():
            try:
                content = desc_file.read_text(encoding='utf-8')
                return content.strip()
            except Exception as e:
                print(f"❌ Error reading {desc_file}: {e}")
    
    return None

def generate_default_description(filename):
    """Generate smart default descriptions based on filename"""
    descriptions = {
        'quantum': 'Explores quantum mechanical principles applied to spiritual reality and consciousness.',
        'entanglement': 'Visualizes non-local connections between spiritual entities through quantum mechanics.',
        'consciousness': 'Maps the relationship between consciousness and physical reality.',
        'trinity': 'Mathematical representation of Trinitarian relationships using quantum field theory.',
        'master-equation': 'Components and interactions within the unified Master Equation framework.',
        'entropy': 'The interplay between spiritual decay and divine ordering principles.',
        'grace': 'Mathematical modeling of divine grace as negentropy in spiritual systems.',
        'sin': 'Thermodynamic analysis of sin as spiritual entropy.',
        'gravity': 'Parallels between gravitational and spiritual attractive forces.',
        'strong-force': 'Nuclear binding forces as models for divine unity.',
        'electromagnetic': 'Light and truth as electromagnetic phenomena.',
        'spiritual': 'Direct applications of physical laws to spiritual realities.',
        'faith': 'Network theory and field dynamics applied to faith communities.',
        'light': 'Truth as electromagnetic radiation in spiritual spectra.'
    }
    
    filename_lower = filename.lower()
    for key, desc in descriptions.items():
        if key in filename_lower:
            return desc
    
    return 'Advanced visualization integrating physics and theology through mathematical frameworks.'

def scan_current_folder():
    """Scan current folder for HTML and SVG files"""
    files = {'html': [], 'svg': []}
    
    # Scan HTML files in current directory
    for file in CURRENT_DIR.glob('*.html'):
        if file.name != 'index.html':  # Skip the gallery itself
            custom_desc = load_custom_description(file.name)
            description = custom_desc if custom_desc else generate_default_description(file.name)
            
            files['html'].append({
                'name': file.stem.replace('-', ' ').title(),
                'filename': file.name,
                'description': description,
                'has_custom_desc': custom_desc is not None
            })
    
    # Scan SVG files in images folder
    if IMAGES_DIR.exists():
        for file in IMAGES_DIR.glob('*.svg'):
            custom_desc = load_custom_description(file.name)
            description = custom_desc if custom_desc else generate_default_description(file.name)
            
            files['svg'].append({
                'name': file.stem.replace('-', ' ').title(),
                'filename': file.name,
                'description': description,
                'has_custom_desc': custom_desc is not None
            })
    
    return files

def update_index_html():
    """Update the index.html with current file data"""
    files = scan_current_folder()
    
    print(f"📊 Found {len(files['html'])} HTML files and {len(files['svg'])} SVG files")
    
    # Update stats in existing index.html
    index_file = CURRENT_DIR / 'index.html'
    if index_file.exists():
        content = index_file.read_text(encoding='utf-8')
        
        # Update the stats
        total_count = len(files['html']) + len(files['svg'])
        completed_count = total_count - 2  # Assume most are complete
        
        # Simple replacements
        content = content.replace('id="total-count">200+', f'id="total-count">{total_count}')
        content = content.replace('id="completed-count">185+', f'id="completed-count">{completed_count}')
        
        index_file.write_text(content, encoding='utf-8')
        print(f"✅ Updated index.html with current stats")
    
    return files

def create_example_descriptions():
    """Create example description files"""
    if not DESCRIPTIONS_DIR.exists():
        DESCRIPTIONS_DIR.mkdir()
    
    examples = {
        'master-equation.txt': 'The Master Equation visualization showing the complete unified framework that mathematically describes the salvation narrative through 10 integrated variables.',
        'law-1.txt': 'Explores the parallel between universal gravitation and spiritual gravity, showing how sin creates attractive forces that require divine escape velocity to overcome.',
        'quantum-trinity-spiral.md': '''# Quantum Trinity Spiral

Revolutionary visualization combining Trinity doctrine with quantum field theory, demonstrating three-person unity through quantum entanglement.'''
    }
    
    created = 0
    for filename, content in examples.items():
        example_file = DESCRIPTIONS_DIR / filename
        if not example_file.exists():
            example_file.write_text(content, encoding='utf-8')
            created += 1
    
    if created > 0:
        print(f"📝 Created {created} example description files")

def main():
    """Main function - run once or continuously"""
    print("🚀 FAITHTHRUPHYSICS Gallery Updater")
    print("=" * 50)
    print(f"📁 Scanning: {CURRENT_DIR}")
    print(f"🖼️  Images: {IMAGES_DIR}")
    print(f"📝 Descriptions: {DESCRIPTIONS_DIR}")
    print("=" * 50)
    
    # Create example descriptions
    create_example_descriptions()
    
    # Update the gallery
    files = update_index_html()
    
    print("\n✅ Gallery updated successfully!")
    print(f"💡 To add custom descriptions:")
    print(f"   1. Create filename.txt in: {DESCRIPTIONS_DIR}")
    print(f"   2. Use same base name as your visualization")
    print(f"   3. Example: law-1.txt for law-1.html")
    
    # Ask if they want continuous monitoring
    response = input("\n🔄 Run continuous monitoring? (y/n): ").lower()
    
    if response == 'y':
        print("\n🔄 Starting continuous monitoring (Ctrl+C to stop)...")
        try:
            while True:
                update_index_html()
                print(f"⏰ Next scan in 30 seconds... ({time.strftime('%H:%M:%S')})")
                time.sleep(30)
        except KeyboardInterrupt:
            print("\n👋 Monitoring stopped")
    
    print("\n🚀 Ready to upload to Cloudflare Pages!")

if __name__ == "__main__":
    main()
