#!/usr/bin/env python3
"""
Generate contact sheets and mapping JSON for language history diagrams.
"""
import xml.etree.ElementTree as ET
import urllib.parse
import base64
import json
import hashlib
import os
import re
import zlib
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# Expected languages by year
EXPECTED_LANGUAGES = {
    1947: "ASM",
    1957: "Fortran",
    1962: "Simula",
    1963: "BASIC",
    1969: "Smalltalk",
    1978: "C",
    1984: "Objective-C",
    1985: "C++",
    1986: "Eiffel",
    1990: "Haskell",
    1991: "Python",
    1995: "Ruby",
    1996: "Java or JavaScript",  # Two icons for 1996
    2000: "C#",
    2003: "Scala",
    2011: "Kotlin",
    2014: "Swift",
    2015: "Rust"
}

def parse_drawio_svg(svg_path):
    """Parse draw.io SVG and extract mxGraphModel."""
    tree = ET.parse(svg_path)
    root = tree.getroot()
    
    content_attr = root.get('content')
    if not content_attr:
        raise ValueError("No content attribute found")
    
    mxfile = ET.fromstring(content_attr)
    diagram = mxfile.find('diagram')
    
    # Check if diagram has mxGraphModel as direct child (uncompressed)
    model = diagram.find('mxGraphModel')
    if model is not None:
        return model
    
    # Compressed format
    diagram_text = diagram.text
    if not diagram_text:
        raise ValueError("No diagram content found")
    
    compressed = base64.b64decode(diagram_text)
    decompressed = zlib.decompress(compressed, -zlib.MAX_WBITS).decode('utf-8')
    decoded = urllib.parse.unquote(decompressed)
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
        
        geom = cell.find('mxGeometry')
        if geom is not None:
            x = float(geom.get('x', 0))
            y = float(geom.get('y', 0))
            w = float(geom.get('width', 0))
            h = float(geom.get('height', 0))
            
            if 'shape=image' in style and 'image=data:image' in style:
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
            
            elif value and value.strip():
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
        candidates = []
        for txt in text_cells:
            if txt['top'] >= img['bottom'] - 20:
                h_dist = abs(txt['center_x'] - img['center_x'])
                v_dist = abs(txt['top'] - img['bottom'])
                
                if h_dist < 200 and v_dist < 50:
                    candidates.append((h_dist, v_dist, txt))
        
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

def decode_image_data(image_data_uri):
    """Decode image from data URI to PIL Image."""
    match = re.match(r'data:image/([^,]+),(.+)', image_data_uri)
    if not match:
        raise ValueError(f"Invalid data URI format")
    
    mime_type = match.group(1)
    data = match.group(2)
    
    image_type = mime_type.split(';')[0].split('+')[0]
    
    # All data appears to be base64 encoded
    try:
        img_bytes = base64.b64decode(data)
    except Exception as e:
        # Try adding padding
        padding = 4 - len(data) % 4
        if padding != 4:
            data += '=' * padding
        img_bytes = base64.b64decode(data)
    
    sha1 = hashlib.sha1(img_bytes).hexdigest()
    
    # Try to load as image
    try:
        if image_type == 'svg':
            # SVG needs special handling - for now create placeholder
            img = Image.new('RGB', (160, 160), 'lightgray')
            draw = ImageDraw.Draw(img)
            draw.text((10, 75), "SVG", fill='black')
            return img, sha1, True
        else:
            img = Image.open(BytesIO(img_bytes))
            if img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGBA')
            # Convert RGBA to RGB on white background
            if img.mode == 'RGBA':
                background = Image.new('RGB', img.size, 'white')
                background.paste(img, mask=img.split()[3])
                img = background
            return img, sha1, False
    except Exception as e:
        print(f"Error loading image: {e}")
        # Return placeholder
        img = Image.new('RGB', (160, 160), 'white')
        draw = ImageDraw.Draw(img)
        draw.text((10, 75), "ERROR", fill='red')
        return img, sha1, False

def create_contact_sheet(matched_items, output_path, title):
    """Create a contact sheet PNG with all icons."""
    # Sort by year
    matched_items.sort(key=lambda x: (int(x['year_label']) if x['year_label'].isdigit() else 9999, x['cell_id']))
    
    # Handle duplicate 1996 entries
    year_counts = {}
    for item in matched_items:
        year = item['year_label']
        year_counts[year] = year_counts.get(year, 0) + 1
    
    year_seen = {}
    
    # Layout: 5 columns
    cols = 5
    rows = (len(matched_items) + cols - 1) // cols
    
    tile_width = 200
    tile_height = 240
    margin = 20
    
    sheet_width = cols * tile_width + (cols + 1) * margin
    sheet_height = rows * tile_height + (rows + 1) * margin + 50  # Extra for title
    
    sheet = Image.new('RGB', (sheet_width, sheet_height), 'white')
    draw = ImageDraw.Draw(sheet)
    
    # Try to load a font
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        label_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except:
        title_font = ImageFont.load_default()
        label_font = ImageFont.load_default()
    
    # Draw title
    draw.text((margin, 15), title, fill='black', font=title_font)
    
    # Draw tiles
    for idx, item in enumerate(matched_items):
        row = idx // cols
        col = idx % cols
        
        x = margin + col * (tile_width + margin)
        y = margin + 50 + row * (tile_height + margin)
        
        # Decode and draw icon
        try:
            img, sha1, is_svg = decode_image_data(item['image_data'])
            # Resize to fit
            img.thumbnail((160, 160), Image.Resampling.LANCZOS)
            # Center in tile
            img_x = x + (tile_width - img.width) // 2
            img_y = y + 10
            sheet.paste(img, (img_x, img_y))
        except Exception as e:
            print(f"Error processing image for cell {item['cell_id']}: {e}")
            # Draw placeholder box
            draw.rectangle([x + 20, y + 10, x + 180, y + 170], outline='red', width=2)
        
        # Draw label
        year = item['year_label']
        cell_id = item['cell_id']
        
        # Handle 1996 duplicates
        if year_counts.get(year, 0) > 1:
            if year not in year_seen:
                year_seen[year] = 0
            year_seen[year] += 1
            suffix = chr(64 + year_seen[year])  # A, B, C...
            label_text = f"cell {cell_id} | {year}{suffix}"
        else:
            label_text = f"cell {cell_id} | {year}"
        
        # Draw label centered
        bbox = draw.textbbox((0, 0), label_text, font=label_font)
        text_width = bbox[2] - bbox[0]
        text_x = x + (tile_width - text_width) // 2
        text_y = y + 185
        draw.text((text_x, text_y), label_text, fill='black', font=label_font)
    
    sheet.save(output_path)
    print(f"Created contact sheet: {output_path}")

def create_mapping_json(matched_items, output_path):
    """Create mapping JSON file."""
    matched_items.sort(key=lambda x: (int(x['year_label']) if x['year_label'].isdigit() else 9999, x['cell_id']))
    
    # Handle duplicate years
    year_counts = {}
    for item in matched_items:
        year = item['year_label']
        year_counts[year] = year_counts.get(year, 0) + 1
    
    year_seen = {}
    
    mapping = []
    for item in matched_items:
        year = item['year_label']
        year_int = int(year) if year.isdigit() else 0
        
        # Get SHA1
        try:
            _, sha1, _ = decode_image_data(item['image_data'])
        except:
            sha1 = "unknown"
        
        # Get expected language
        language = EXPECTED_LANGUAGES.get(year_int, "UNKNOWN")
        
        entry = {
            "cell_id": item['cell_id'],
            "year": year,
            "x": item['x'],
            "y": item['y'],
            "w": item['w'],
            "h": item['h'],
            "image_sha1": sha1,
            "language_by_year": language
        }
        
        mapping.append(entry)
    
    with open(output_path, 'w') as f:
        json.dump(mapping, f, indent=2)
    
    print(f"Created mapping JSON: {output_path}")
    
    return mapping

def main():
    files = [
        ('lectures/Einführung AIN/diagrams/language-history.drawio.svg', 'erst', 'Einführung AIN'),
        ('lectures/programmiertechnik-I/diagrams/language-history.drawio.svg', 'pt1', 'Programmiertechnik I')
    ]
    
    os.makedirs('/opt/cursor/artifacts', exist_ok=True)
    
    for svg_file, short_name, full_name in files:
        print(f"\n{'='*60}")
        print(f"Processing {svg_file}")
        print('='*60)
        
        # Parse
        model = parse_drawio_svg(svg_file)
        image_cells, text_cells = extract_cells(model)
        print(f"Found {len(image_cells)} image cells and {len(text_cells)} text cells")
        
        # Match
        matched = match_icons_to_years(image_cells, text_cells)
        print(f"Matched {len(matched)} icons to year labels")
        
        # Create contact sheet
        contact_path = f'/opt/cursor/artifacts/contact_{short_name}.png'
        create_contact_sheet(matched, contact_path, f"{full_name} Language History")
        
        # Create mapping JSON
        json_path = f'/opt/cursor/artifacts/mapping_{short_name}.json'
        mapping = create_mapping_json(matched, json_path)
        
        # Print table
        print(f"\nTable for {short_name}:")
        print("cell_id | year")
        print("-" * 20)
        for entry in mapping:
            print(f"{entry['cell_id']:7} | {entry['year']}")

if __name__ == '__main__':
    main()
