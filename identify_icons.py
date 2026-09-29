#!/usr/bin/env python3
"""
Extract and identify each icon from the original diagrams by:
1. Finding nearby year labels to determine which language
2. Extracting the actual image data
3. Saving each icon as a separate file for visual inspection
"""

import xml.etree.ElementTree as ET
import base64
import zlib
import urllib.parse
import re
import json
from pathlib import Path

def extract_mxfile_content(svg_path):
    """Extract the mxfile content from SVG."""
    tree = ET.parse(svg_path)
    root = tree.getroot()
    content = root.get('content')
    
    if not content:
        raise ValueError("No content attribute in SVG")
    
    if content.startswith('<mxfile'):
        return content, False
    
    try:
        decoded = base64.b64decode(content)
        decompressed = zlib.decompress(decoded, -zlib.MAX_WBITS)
        return decompressed.decode('utf-8'), True
    except:
        return urllib.parse.unquote(content), False

def parse_mxfile(mxfile_xml):
    """Parse mxfile XML and extract the diagram."""
    mxfile = ET.fromstring(mxfile_xml)
    diagram = mxfile.find('diagram')
    if diagram is None:
        raise ValueError("No diagram found")
    
    # Check if mxGraphModel is directly a child of diagram
    model = diagram.find('mxGraphModel')
    if model is not None:
        return model
    
    diagram_content = diagram.text
    if not diagram_content:
        raise ValueError("Empty diagram")
    
    try:
        decoded = base64.b64decode(diagram_content)
        decompressed = zlib.decompress(decoded, -zlib.MAX_WBITS)
        model_xml = decompressed.decode('utf-8')
    except:
        try:
            decoded = base64.b64decode(diagram_content)
            model_xml = decoded.decode('utf-8')
        except:
            model_xml = diagram_content
    
    if '%' in model_xml and '<' not in model_xml[:100]:
        model_xml = urllib.parse.unquote(model_xml)
    
    return ET.fromstring(model_xml)

def extract_year_from_value(value):
    """Extract a 4-digit year from HTML-embedded text."""
    # Look for 4-digit years in the value
    match = re.search(r'\b(19\d{2}|20\d{2})\b', value)
    if match:
        return int(match.group(1))
    return None

def identify_icons(svg_path, output_dir):
    """Identify each icon by finding nearby year labels."""
    
    mxfile_xml, _ = extract_mxfile_content(svg_path)
    model = parse_mxfile(mxfile_xml)
    root = model.find('root')
    
    cells = []
    for cell in root.findall('mxCell'):
        cell_id = cell.get('id')
        value = cell.get('value', '')
        style = cell.get('style', '')
        
        geom = cell.find('mxGeometry')
        x, y, width, height = 0, 0, 0, 0
        if geom is not None:
            x = float(geom.get('x', 0))
            y = float(geom.get('y', 0))
            width = float(geom.get('width', 0))
            height = float(geom.get('height', 0))
        
        info = {
            'id': cell_id,
            'value': value,
            'style': style,
            'x': x,
            'y': y,
            'width': width,
            'height': height,
            'is_image': 'image=' in style or 'shape=image' in style,
            'is_text': bool(value),
            'year': extract_year_from_value(value) if value else None
        }
        
        if info['is_image']:
            match = re.search(r'image=([^;]+)', style)
            if match:
                info['image_ref'] = match.group(1)
        
        cells.append(info)
    
    # Get all icons and year labels
    icons = [c for c in cells if c['is_image']]
    year_labels = [c for c in cells if c['year'] is not None]
    
    print(f"Found {len(icons)} icons and {len(year_labels)} year labels")
    
    # Language to year mapping
    lang_years = {
        1947: 'ASM',
        1957: 'Fortran', 
        1962: 'Simula',
        1963: 'BASIC',
        1969: 'Smalltalk',
        1978: 'C',
        1984: 'Objective-C',
        1985: 'C++',
        1986: 'Eiffel',
        1990: 'Haskell',
        1991: 'Python',
        1995: 'Ruby',
        1996: 'Java',  # First 1996
        2000: 'C#',
        2003: 'Scala',
        2011: 'Kotlin',
        2014: 'Swift',
        2015: 'Rust'
    }
    
    # For each icon, find the closest year label
    icon_mappings = []
    
    for icon in icons:
        icon_center_x = icon['x'] + icon['width'] / 2
        icon_center_y = icon['y'] + icon['height'] / 2
        
        # Find closest year label
        closest_year = None
        closest_dist = float('inf')
        
        for year_label in year_labels:
            label_center_x = year_label['x'] + year_label['width'] / 2
            label_center_y = year_label['y'] + year_label['height'] / 2
            
            # Calculate distance
            dist = ((icon_center_x - label_center_x)**2 + (icon_center_y - label_center_y)**2)**0.5
            
            if dist < closest_dist:
                closest_dist = dist
                closest_year = year_label['year']
        
        # Determine language name
        lang_name = lang_years.get(closest_year, f"Unknown_{closest_year}")
        
        # Handle JavaScript (second 1996)
        if closest_year == 1996:
            # Check if we already have a Java icon
            existing_1996 = [m for m in icon_mappings if m['year'] == 1996]
            if existing_1996:
                lang_name = 'JavaScript'
        
        mapping = {
            'language': lang_name,
            'year': closest_year,
            'icon_x': icon['x'],
            'icon_y': icon['y'],
            'icon_width': icon['width'],
            'icon_height': icon['height'],
            'image_ref': icon.get('image_ref', ''),
            'distance_to_year': closest_dist
        }
        
        icon_mappings.append(mapping)
        
        # Save the icon image if it's a data URL
        image_ref = icon.get('image_ref', '')
        if image_ref.startswith('data:image/'):
            try:
                # Parse data URL
                match = re.match(r'data:image/([^;,]+);?([^,]*),(.+)', image_ref)
                if match:
                    img_format = match.group(1)
                    encoding = match.group(2)
                    img_data = match.group(3)
                    
                    # Decode
                    if 'base64' in encoding:
                        img_bytes = base64.b64decode(img_data)
                    else:
                        img_bytes = urllib.parse.unquote(img_data).encode()
                    
                    # Save
                    output_path = Path(output_dir) / f"{closest_year}_{lang_name}.{img_format.replace('svg+xml', 'svg')}"
                    with open(output_path, 'wb') as f:
                        f.write(img_bytes)
                    
                    print(f"  Saved icon: {output_path.name} ({len(img_bytes)} bytes)")
            except Exception as e:
                print(f"  Error saving icon for {lang_name}: {e}")
    
    # Sort by year
    icon_mappings.sort(key=lambda m: (m['year'], m['language']))
    
    return icon_mappings

def main():
    import sys
    if len(sys.argv) < 3:
        print("Usage: python identify_icons.py <input.svg> <output_dir>")
        sys.exit(1)
    
    svg_path = sys.argv[1]
    output_dir = sys.argv[2]
    
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    print(f"Analyzing {svg_path}...")
    mappings = identify_icons(svg_path, output_dir)
    
    print(f"\nIcon-to-language mappings ({len(mappings)} total):")
    print("="*80)
    for m in mappings:
        print(f"{m['year']}: {m['language']:15} @ ({int(m['icon_x']):4}, {int(m['icon_y']):3}) "
              f"- distance to year label: {m['distance_to_year']:.1f}px")
    
    # Save to JSON
    json_path = Path(output_dir) / 'icon_mappings.json'
    with open(json_path, 'w') as f:
        json.dump(mappings, f, indent=2)
    print(f"\nSaved mappings to {json_path}")

if __name__ == '__main__':
    main()
