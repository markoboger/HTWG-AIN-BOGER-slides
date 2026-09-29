#!/usr/bin/env python3
"""
Extract icon mappings from the original draw.io SVG files.
This will help us map which icon belongs to which language.
"""

import xml.etree.ElementTree as ET
import base64
import zlib
import urllib.parse
import sys
import re
import json

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
        # Uncompressed format (Erstsemester)
        return model
    
    # Otherwise, it's in the diagram text
    diagram_content = diagram.text
    if not diagram_content:
        raise ValueError("Empty diagram and no mxGraphModel child")
    
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

def extract_all_info(model):
    """Extract all icons and text labels to figure out mappings."""
    root = model.find('root')
    if root is None:
        return []
    
    cells_info = []
    
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
            'is_text': 'text;' in style or value != ''
        }
        
        if info['is_image']:
            # Extract image reference
            match = re.search(r'image=([^;]+)', style)
            if match:
                info['image_ref'] = match.group(1)
        
        cells_info.append(info)
    
    return cells_info

def find_icon_mappings(cells_info):
    """Try to determine which icon corresponds to which language."""
    # Sort by Y position (top to bottom), then X (left to right)
    images = [c for c in cells_info if c['is_image']]
    images.sort(key=lambda c: (c['y'], c['x']))
    
    # Look for nearby text labels
    texts = [c for c in cells_info if c['is_text'] and c['value']]
    
    mappings = []
    for img in images:
        # Find text within ~100 pixels vertically
        nearby_texts = [
            t for t in texts 
            if abs(t['x'] + t['width']/2 - img['x'] - img['width']/2) < 100
            and abs(t['y'] - img['y']) < 150
        ]
        
        # Find the closest one vertically
        if nearby_texts:
            nearest = min(nearby_texts, key=lambda t: abs(t['y'] - img['y']))
            label = nearest['value']
        else:
            label = f"Icon at ({int(img['x'])}, {int(img['y'])})"
        
        mappings.append({
            'label': label,
            'image_ref': img.get('image_ref', ''),
            'x': img['x'],
            'y': img['y'],
            'width': img['width'],
            'height': img['height']
        })
    
    return mappings

def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_icons.py <input.drawio.svg>")
        sys.exit(1)
    
    input_svg = sys.argv[1]
    
    print(f"Extracting icon mappings from {input_svg}...")
    
    mxfile_xml, was_compressed = extract_mxfile_content(input_svg)
    model = parse_mxfile(mxfile_xml)
    cells_info = extract_all_info(model)
    
    print(f"Found {len(cells_info)} cells total")
    print(f"Images: {sum(1 for c in cells_info if c['is_image'])}")
    print(f"Text labels: {sum(1 for c in cells_info if c['is_text'] and c['value'])}")
    
    mappings = find_icon_mappings(cells_info)
    
    print(f"\nIcon mappings ({len(mappings)} icons):")
    print("="*80)
    for i, m in enumerate(mappings, 1):
        img_ref_preview = m['image_ref'][:80] + ('...' if len(m['image_ref']) > 80 else '')
        print(f"{i:2}. {m['label']:20} @ ({int(m['x']):4}, {int(m['y']):4})")
        print(f"    Image: {img_ref_preview}")
        print()
    
    # Save to JSON
    output_json = input_svg.replace('.svg', '_icons.json')
    with open(output_json, 'w') as f:
        json.dump(mappings, f, indent=2)
    print(f"Saved mappings to {output_json}")

if __name__ == '__main__':
    main()
