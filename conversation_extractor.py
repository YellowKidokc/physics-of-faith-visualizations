import json
import re
import os
from pathlib import Path
import html

def extract_visualizations_from_conversation(json_file_path, output_dir="extracted_visualizations"):
    """
    Intelligently extracts SVG and HTML visualizations from Claude conversation history JSON
    """
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    print(f"🔍 Loading conversation history from: {json_file_path}")
    
    # Load the JSON file
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ JSON loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading JSON: {e}")
        return
    
    # Initialize counters
    svg_count = 0
    html_count = 0
    total_visualizations = 0
    
    # Function to clean and create filename
    def create_filename(title, content_type, index):
        if not title:
            return f"{content_type}_visualization_{index}"
        
        # Clean title for filename
        filename = re.sub(r'[^\w\s-]', '', title.strip())
        filename = re.sub(r'[-\s]+', '_', filename)
        filename = filename.lower()
        
        # Limit length
        if len(filename) > 50:
            filename = filename[:50]
        
        return f"{filename}_{content_type}"
    
    # Function to extract title from context
    def extract_title_from_context(messages, current_index):
        """Look for titles in nearby messages"""
        title_patterns = [
            r'title["\']?\s*[:=]\s*["\']([^"\']+)["\']',
            r'<title[^>]*>([^<]+)</title>',
            r'# ([^\n]+)',
            r'## ([^\n]+)',
            r'### ([^\n]+)',
        ]
        
        # Check current and previous few messages for titles
        start_idx = max(0, current_index - 3)
        end_idx = min(len(messages), current_index + 2)
        
        for i in range(start_idx, end_idx):
            message_content = str(messages[i].get('content', ''))
            
            for pattern in title_patterns:
                matches = re.findall(pattern, message_content, re.IGNORECASE | re.MULTILINE)
                if matches:
                    return matches[0].strip()
        
        return None
    
    # Function to extract SVG content
    def extract_svg_content(content):
        """Extract complete SVG content"""
        svg_pattern = r'<svg[^>]*>.*?</svg>'
        matches = re.findall(svg_pattern, content, re.DOTALL | re.IGNORECASE)
        return matches
    
    # Function to extract HTML content
    def extract_html_content(content):
        """Extract complete HTML documents"""
        html_pattern = r'<!DOCTYPE html>.*?</html>'
        matches = re.findall(html_pattern, content, re.DOTALL | re.IGNORECASE)
        return matches
    
    # Function to create complete HTML wrapper for SVG
    def wrap_svg_in_html(svg_content, title):
        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            background: #000;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            font-family: Arial, sans-serif;
        }}
        svg {{
            max-width: 100%;
            max-height: 100vh;
            border: 1px solid #333;
        }}
    </style>
</head>
<body>
    {svg_content}
</body>
</html>"""
        return html_template
    
    # Process the conversation
    if isinstance(data, list):
        messages = data
    elif isinstance(data, dict) and 'messages' in data:
        messages = data['messages']
    elif isinstance(data, dict) and 'conversation' in data:
        messages = data['conversation']
    else:
        # Try to find any array of messages
        for key, value in data.items():
            if isinstance(value, list) and len(value) > 0:
                if isinstance(value[0], dict) and 'content' in value[0]:
                    messages = value
                    break
        else:
            print("❌ Could not find messages in JSON structure")
            print(f"Available keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
            return
    
    print(f"📝 Processing {len(messages)} messages...")
    
    # Extract visualizations from each message
    for i, message in enumerate(messages):
        content = str(message.get('content', ''))
        
        # Skip if no content
        if not content:
            continue
        
        # Extract SVGs
        svg_matches = extract_svg_content(content)
        for svg in svg_matches:
            svg_count += 1
            total_visualizations += 1
            
            # Try to extract title
            title = extract_title_from_context(messages, i)
            if not title:
                title = f"Physics of Faith SVG {svg_count}"
            
            filename = create_filename(title, "svg", svg_count)
            
            # Wrap SVG in complete HTML
            html_content = wrap_svg_in_html(svg, title)
            
            # Save file
            file_path = output_path / f"{filename}.html"
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                print(f"✅ Saved SVG: {file_path}")
            except Exception as e:
                print(f"❌ Error saving SVG: {e}")
        
        # Extract HTML documents
        html_matches = extract_html_content(content)
        for html_doc in html_matches:
            html_count += 1
            total_visualizations += 1
            
            # Try to extract title from HTML
            title_match = re.search(r'<title[^>]*>([^<]+)</title>', html_doc, re.IGNORECASE)
            if title_match:
                title = title_match.group(1)
            else:
                title = extract_title_from_context(messages, i)
                if not title:
                    title = f"Physics of Faith HTML {html_count}"
            
            filename = create_filename(title, "html", html_count)
            
            # Save file
            file_path = output_path / f"{filename}.html"
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(html_doc)
                print(f"✅ Saved HTML: {file_path}")
            except Exception as e:
                print(f"❌ Error saving HTML: {e}")
    
    # Create index file
    create_index_file(output_path, total_visualizations)
    
    print(f"\n🎉 EXTRACTION COMPLETE!")
    print(f"📊 Statistics:")
    print(f"   • SVG files: {svg_count}")
    print(f"   • HTML files: {html_count}")
    print(f"   • Total visualizations: {total_visualizations}")
    print(f"   • Output directory: {output_path.absolute()}")
    
    return output_path

def create_index_file(output_path, total_count):
    """Create an index.html file listing all visualizations"""
    
    # Get all HTML files
    html_files = list(output_path.glob("*.html"))
    
    index_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Physics of Faith - All Visualizations</title>
    <style>
        body {{
            background: linear-gradient(135deg, #000011 0%, #001122 50%, #000033 100%);
            color: #FFFFFF;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 40px 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        h1 {{
            text-align: center;
            font-size: 3em;
            background: linear-gradient(45deg, #FFD700, #FFA500, #FFD700);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 20px;
        }}
        
        .subtitle {{
            text-align: center;
            font-size: 1.2em;
            color: #CCCCCC;
            margin-bottom: 40px;
        }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 30px;
            margin-top: 40px;
        }}
        
        .card {{
            background: rgba(0, 0, 0, 0.7);
            border: 2px solid rgba(255, 215, 0, 0.3);
            border-radius: 15px;
            padding: 25px;
            transition: all 0.3s ease;
            cursor: pointer;
        }}
        
        .card:hover {{
            border-color: #FFD700;
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(255, 215, 0, 0.3);
        }}
        
        .card h3 {{
            color: #FFD700;
            margin: 0 0 15px 0;
            font-size: 1.3em;
        }}
        
        .card p {{
            color: #CCCCCC;
            margin: 0 0 20px 0;
            line-height: 1.5;
        }}
        
        .launch-btn {{
            background: linear-gradient(45deg, #FFD700, #FFA500);
            color: #000;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            width: 100%;
            font-size: 1em;
        }}
        
        .launch-btn:hover {{
            background: linear-gradient(45deg, #FFA500, #FF6B35);
        }}
        
        .stats {{
            text-align: center;
            margin: 30px 0;
            padding: 20px;
            background: rgba(255, 215, 0, 0.1);
            border-radius: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>PHYSICS OF FAITH</h1>
        <p class="subtitle">Complete Visualization Collection</p>
        
        <div class="stats">
            <h2>📊 {total_count} Visualizations Extracted</h2>
            <p>All visualizations from your conversation history, automatically extracted and ready to deploy!</p>
        </div>
        
        <div class="grid">
"""
    
    # Add cards for each visualization
    for html_file in sorted(html_files):
        if html_file.name == "index.html":
            continue
            
        # Clean up filename for display
        display_name = html_file.stem.replace('_', ' ').title()
        
        index_content += f"""
            <div class="card" onclick="window.open('{html_file.name}', '_blank')">
                <h3>{display_name}</h3>
                <p>Interactive visualization from the Physics of Faith framework</p>
                <button class="launch-btn">Launch Visualization</button>
            </div>
"""
    
    index_content += """
        </div>
        
        <div style="text-align: center; margin-top: 50px; color: #666;">
            <p>🚀 Ready to deploy to Cloudflare Pages!</p>
        </div>
    </div>
</body>
</html>"""
    
    # Save index file
    index_path = output_path / "index.html"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"✅ Created index file: {index_path}")

# Example usage
if __name__ == "__main__":
    print("🎯 Physics of Faith Visualization Extractor")
    print("=" * 50)
    
    # Get JSON file path from user
    json_path = input("📁 Enter path to your conversation JSON file: ").strip().strip('"')
    
    if not os.path.exists(json_path):
        print(f"❌ File not found: {json_path}")
        exit(1)
    
    # Extract visualizations
    output_dir = extract_visualizations_from_conversation(json_path)
    
    print(f"\n🎉 SUCCESS! All visualizations extracted to: {output_dir}")
    print(f"📋 Next steps:")
    print(f"   1. Zip the '{output_dir}' folder")
    print(f"   2. Upload to Cloudflare Pages")
    print(f"   3. Your Physics of Faith site will be live!")
