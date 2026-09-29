#!/usr/bin/env python3
"""
Parse language-history.drawio.svg files to map icon cells to languages.
"""
import xml.etree.ElementTree as ET
import urllib.parse
import base64
import json
import hashlib
import os
import re
import html
import zlib
from pathlib import Path

def parse_drawio_svg(svg_path):
    """Parse draw.io SVG and extract mxGraphModel."""
    tree = ET.parse(svg_path)
    root = tree.getroot()
    
    # Find content attribute
    content_attr = root.get('content')
    if not content_attr:
        raise ValueError("No content attribute found")
    
    # Parse mxfile XML
    mxfile = ET.fromstring(content_attr)
    diagram = mxfile.find('diagram')
    
    # Check if diagram has mxGraphModel as direct child (uncompressed)
    model = diagram.find('mxGraphModel')
    if model is not None:
        return model
    
    # Otherwise, diagram content is compressed in text
    diagram_text = diagram.text
    if not diagram_text:
        raise ValueError("No diagram content found")
    
    # Compressed format - decode base64 and inflate
    compressed = base64.b64decode(diagram_text)
    decompressed = zlib.decompress(compressed, -zlib.MAX_WBITS).decode('utf-8')
    
    # URL decode (no HTML unescape needed for compressed format)
    decoded = urllib.parse.unquote(decompressed)
    
    # Parse as mxGraphModel
    model = ET.fromstring(decoded)
    
    return model

def extract_cells(model):
    """Extract image and text cells from model."""
    root = model.find('root')
    
    image_cells = []
    text_cells = []
    
    for cell in root.findall('mxCell'):
        cell_id = cell.get('id')
        style = cell.get('style', '')
        value = cell.get('value', '')
        
        # Get geometry
        geom = cell.find('mxGeometry')
        if geom is not None:
            x = float(geom.get('x', 0))
            y = float(geom.get('y', 0))
            w = float(geom.get('width', 0))
            h = float(geom.get('height', 0))
            
            # Check if it's an image cell
            if 'shape=image' in style and 'image=data:image' in style:
                # Extract image data from style - supports both base64 and raw formats
                match = re.search(r'image=(data:image/[^;,]+[;,][^;]+?)(?:;|$)', style)
                if match:
                    image_data = match.group(1)
                    image_cells.append({
                        'id': cell_id,
                        'x': x,
                        'y': y,
                        'w': w,
                        'h': h,
                        'center_x': x + w/2,
                        'center_y': y + h/2,
                        'bottom': y + h,
                        'image_data': image_data
                    })
            
            # Check if it's a text cell with a value
            elif value and value.strip():
                # Extract year from value (plain text or HTML)
                year_match = re.search(r'\b(194\d|195\d|196\d|197\d|198\d|199\d|200\d|201\d|202\d)\b', value)
                if year_match:
                    year = year_match.group(1)
                    text_cells.append({
                        'id': cell_id,
                        'x': x,
                        'y': y,
                        'w': w,
                        'h': h,
                        'center_x': x + w/2,
                        'center_y': y + h/2,
                        'top': y,
                        'value': year
                    })
    
    return image_cells, text_cells

def match_icons_to_years(image_cells, text_cells):
    """Match each image to its year label below it."""
    matched = []
    
    for img in image_cells:
        # Find text cells that could be below this image
        # More lenient: y of text just needs to be >= bottom of image
        candidates = []
        for txt in text_cells:
            # Must be at same y level or below  
            if txt['top'] >= img['bottom'] - 20:  # Allow small overlap
                # Calculate horizontal distance
                h_dist = abs(txt['center_x'] - img['center_x'])
                v_dist = abs(txt['top'] - img['bottom'])
                
                # Much more lenient horizontal and vertical matching
                if h_dist < 200 and v_dist < 50:
                    candidates.append((h_dist, v_dist, txt))
        
        # Sort by total distance (horizontal + vertical)
        candidates.sort(key=lambda x: x[0] + x[1])
        
        if candidates:
            year_label = candidates[0][2]['value']
        else:
            year_label = 'UNKNOWN'
        
        matched.append({
            'cell_id': img['id'],
            'x': img['x'],
            'y': img['y'],
            'w': img['w'],
            'h': img['h'],
            'year_label': year_label,
            'image_data': img['image_data']
        })
    
    return matched

def save_image(image_data_uri, output_path):
    """Save image from data URI to file."""
    # Parse data URI - support both base64 and raw formats
    # Format 1: data:image/png;base64,<base64data>
    # Format 2: data:image/svg+xml,<base64data>
    # Format 3: data:image/png,<rawdata>
    match = re.match(r'data:image/([^,]+),(.+)', image_data_uri)
    if not match:
        raise ValueError(f"Invalid data URI format: {image_data_uri[:100]}")
    
    mime_type = match.group(1)  # e.g., "png", "svg+xml", "png;base64"
    data = match.group(2)
    
    # Extract image type
    image_type = mime_type.split(';')[0].split('+')[0]  # "svg+xml" -> "svg", "png;base64" -> "png"
    
    # Check if it looks like base64 (SVGs are base64 even without ;base64 marker)
    if ';base64' in mime_type or image_type == 'svg':
        # Decode base64
        img_bytes = base64.b64decode(data)
    else:
        # Raw data - already decoded (for PNG with raw data)
        img_bytes = data.encode('latin-1')
    
    # Calculate SHA1
    sha1 = hashlib.sha1(img_bytes).hexdigest()
    
    # Save to file
    with open(output_path, 'wb') as f:
        f.write(img_bytes)
    
    return sha1, image_type

def main():
    files = [
        ('lectures/Einführung AIN/diagrams/language-history.drawio.svg', 'erst'),
        ('lectures/programmiertechnik-I/diagrams/language-history.drawio.svg', 'pt1')
    ]
    
    for svg_file, short_name in files:
        print(f"\n=== Processing {svg_file} ===")
        
        # Parse SVG
        model = parse_drawio_svg(svg_file)
        
        # Extract cells
        image_cells, text_cells = extract_cells(model)
        print(f"Found {len(image_cells)} image cells and {len(text_cells)} text cells")
        
        # Match icons to years
        matched = match_icons_to_years(image_cells, text_cells)
        print(f"Matched {len(matched)} icons to year labels")
        
        # Sort by year for easier processing
        matched.sort(key=lambda x: int(x['year_label']) if x['year_label'].isdigit() else 9999)
        
        # Extract images
        for item in matched:
            cell_id = item['cell_id']
            year = item['year_label']
            
            # Create output filename
            output_name = f"{short_name}_{cell_id}_{year}"
            output_path = f"/tmp/{output_name}.img"
            
            sha1, img_type = save_image(item['image_data'], output_path)
            item['sha1'] = sha1
            item['img_type'] = img_type
            item['tmp_path'] = output_path
            
            print(f"  Cell {cell_id}: year={year}, sha1={sha1[:8]}..., type={img_type}")
        
        # Save intermediate data
        with open(f'/tmp/matched_{short_name}.json', 'w') as f:
            json.dump(matched, f, indent=2)

if __name__ == '__main__':
    main()
