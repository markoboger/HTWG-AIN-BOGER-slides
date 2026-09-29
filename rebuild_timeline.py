#!/usr/bin/env python3
"""
Rebuild language timeline diagrams in draw.io format.
This script:
1. Extracts the mxGraphModel from the SVG
2. Extracts all existing icon image data
3. Rebuilds the diagram with proper timeline layout
4. Saves as a temporary .drawio file
5. Exports back to SVG using draw.io CLI
"""

import xml.etree.ElementTree as ET
import base64
import zlib
import urllib.parse
import sys
import re
from pathlib import Path

# Language data
LANGUAGES = [
    ('ASM', 1947),
    ('Fortran', 1957),
    ('Simula', 1962),
    ('BASIC', 1963),
    ('Smalltalk', 1969),
    ('C', 1978),
    ('Objective-C', 1984),
    ('C++', 1985),
    ('Eiffel', 1986),
    ('Haskell', 1990),
    ('Python', 1991),
    ('Ruby', 1995),
    ('Java', 1996),
    ('JavaScript', 1996),
    ('C#', 2000),
    ('Scala', 2003),
    ('Kotlin', 2011),
    ('Swift', 2014),
    ('Rust', 2015),
]

YEARS = sorted(set(year for _, year in LANGUAGES))

# Canvas settings
CANVAS_WIDTH = 1400
CANVAS_HEIGHT = 750
AXIS_Y = 680
MARGIN_LEFT = 60
MARGIN_RIGHT = 60

def extract_mxfile_content(svg_path):
    """Extract the mxfile content from SVG."""
    tree = ET.parse(svg_path)
    root = tree.getroot()
    content = root.get('content')
    
    if not content:
        raise ValueError("No content attribute in SVG")
    
    # Check if compressed or not
    if content.startswith('<mxfile'):
        return content, False
    
    # Try base64+deflate
    try:
        decoded = base64.b64decode(content)
        decompressed = zlib.decompress(decoded, -zlib.MAX_WBITS)
        return decompressed.decode('utf-8'), True
    except:
        # URL-encoded?
        return urllib.parse.unquote(content), False

def parse_mxfile(mxfile_xml):
    """Parse mxfile XML and extract the diagram."""
    mxfile = ET.fromstring(mxfile_xml)
    diagram = mxfile.find('diagram')
    if diagram is None:
        raise ValueError("No diagram found in mxfile")
    
    # The diagram text contains the base64-encoded mxGraphModel
    diagram_content = diagram.text
    if not diagram_content:
        raise ValueError("Empty diagram")
    
    # Decode the diagram content
    try:
        decoded = base64.b64decode(diagram_content)
        decompressed = zlib.decompress(decoded, -zlib.MAX_WBITS)
        model_xml = decompressed.decode('utf-8')
    except:
        # Maybe it's not compressed
        try:
            decoded = base64.b64decode(diagram_content)
            model_xml = decoded.decode('utf-8')
        except:
            model_xml = diagram_content
    
    # Remove URL encoding if present
    if '%' in model_xml and '<' not in model_xml[:100]:
        model_xml = urllib.parse.unquote(model_xml)
    
    return ET.fromstring(model_xml)

def extract_icon_images(model):
    """Extract all icon images from the existing model."""
    icons = {}
    
    root = model.find('root')
    if root is None:
        return icons
    
    for cell in root.findall('mxCell'):
        style = cell.get('style', '')
        value = cell.get('value', '')
        
        # Look for image cells
        if 'image=' in style or 'shape=image' in style:
            # Extract image URL/data from style
            match = re.search(r'image=([^;]+)', style)
            if match:
                image_data = match.group(1)
                # The value might contain the language name or it might be in the style
                # Let's store by the image data itself for now
                icons[cell.get('id')] = {
                    'image': image_data,
                    'value': value,
                    'style': style,
                    'cell': cell
                }
    
    return icons

def guess_language_from_icon(icon_info, all_icons):
    """Try to guess which language an icon represents."""
    # This is heuristic - we'll try to match based on style or position
    # For now, return None and we'll map manually
    return None

def build_new_model(old_icons):
    """Build a completely new mxGraphModel with proper timeline layout."""
    
    # Create the mxGraphModel structure
    model = ET.Element('mxGraphModel')
    model.set('dx', '0')
    model.set('dy', '0')
    model.set('grid', '1')
    model.set('gridSize', '10')
    model.set('guides', '1')
    model.set('tooltips', '1')
    model.set('connect', '1')
    model.set('arrows', '1')
    model.set('fold', '1')
    model.set('page', '1')
    model.set('pageScale', '1')
    model.set('pageWidth', str(CANVAS_WIDTH))
    model.set('pageHeight', str(CANVAS_HEIGHT))
    model.set('math', '0')
    model.set('shadow', '0')
    
    root = ET.SubElement(model, 'root')
    
    # Add the two base cells (required by draw.io)
    cell0 = ET.SubElement(root, 'mxCell')
    cell0.set('id', '0')
    
    cell1 = ET.SubElement(root, 'mxCell')
    cell1.set('id', '1')
    cell1.set('parent', '0')
    
    # Calculate layout
    usable_width = CANVAS_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
    slot_width = usable_width / len(YEARS)
    
    cell_id = 100
    
    # Draw axis line
    axis_cell = ET.SubElement(root, 'mxCell')
    axis_cell.set('id', str(cell_id))
    cell_id += 1
    axis_cell.set('value', '')
    axis_cell.set('style', 'shape=line;strokeWidth=2;strokeColor=#CC0000;')
    axis_cell.set('vertex', '1')
    axis_cell.set('parent', '1')
    axis_geom = ET.SubElement(axis_cell, 'mxGeometry')
    axis_geom.set('x', str(MARGIN_LEFT))
    axis_geom.set('y', str(AXIS_Y))
    axis_geom.set('width', str(usable_width))
    axis_geom.set('height', '1')
    axis_geom.set('as', 'geometry')
    
    # Add year ticks and labels
    for i, year in enumerate(YEARS):
        tick_x = MARGIN_LEFT + i * slot_width
        
        # Tick mark
        tick_cell = ET.SubElement(root, 'mxCell')
        tick_cell.set('id', str(cell_id))
        cell_id += 1
        tick_cell.set('value', '')
        tick_cell.set('style', 'shape=line;strokeWidth=2;strokeColor=#CC0000;direction=south;')
        tick_cell.set('vertex', '1')
        tick_cell.set('parent', '1')
        tick_geom = ET.SubElement(tick_cell, 'mxGeometry')
        tick_geom.set('x', str(tick_x))
        tick_geom.set('y', str(AXIS_Y))
        tick_geom.set('width', '1')
        tick_geom.set('height', '10')
        tick_geom.set('as', 'geometry')
        
        # Year label (below axis)
        year_cell = ET.SubElement(root, 'mxCell')
        year_cell.set('id', str(cell_id))
        cell_id += 1
        year_cell.set('value', str(year))
        year_cell.set('style', 'text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=top;whiteSpace=wrap;fontSize=12;fontColor=#CC0000;fontStyle=0')
        year_cell.set('vertex', '1')
        year_cell.set('parent', '1')
        year_geom = ET.SubElement(year_cell, 'mxGeometry')
        year_geom.set('x', str(tick_x - 20))
        year_geom.set('y', str(AXIS_Y + 12))
        year_geom.set('width', '40')
        year_geom.set('height', '20')
        year_geom.set('as', 'geometry')
    
    # Layout languages
    icon_size = 70
    name_height = 25
    
    # Row heights (staggered)
    row_heights = [100, 250, 400]
    
    # We need to map language names to icon image data from old_icons
    # Since we don't have an easy way to determine which icon is which,
    # we'll use placeholder images for now and indicate where manual mapping is needed
    lang_to_icon = {}
    
    # Try to extract icons in order if they exist
    icon_list = list(old_icons.values())
    for idx, (lang_name, year) in enumerate(LANGUAGES):
        if idx < len(icon_list):
            lang_to_icon[lang_name] = icon_list[idx]['image']
        else:
            # Placeholder
            lang_to_icon[lang_name] = 'https://via.placeholder.com/70'
    
    # Place each language
    for idx, (lang_name, year) in enumerate(LANGUAGES):
        year_idx = YEARS.index(year)
        tick_x = MARGIN_LEFT + year_idx * slot_width
        
        # Determine row (stagger by chronological index, special case for 1996)
        if year == 1996:
            row = 0 if lang_name == 'Java' else 1
        else:
            row = idx % 3
        
        icon_y = row_heights[row]
        icon_x = tick_x - icon_size / 2
        
        # Vertical line from axis to bottom of name label
        line_bottom_y = icon_y + icon_size + name_height + 5
        line_height = AXIS_Y - line_bottom_y
        
        if line_height > 0:
            line_cell = ET.SubElement(root, 'mxCell')
            line_cell.set('id', str(cell_id))
            cell_id += 1
            line_cell.set('value', '')
            line_cell.set('style', 'shape=line;strokeWidth=1;strokeColor=#CC0000;direction=south;')
            line_cell.set('vertex', '1')
            line_cell.set('parent', '1')
            line_geom = ET.SubElement(line_cell, 'mxGeometry')
            line_geom.set('x', str(tick_x))
            line_geom.set('y', str(line_bottom_y))
            line_geom.set('width', '1')
            line_geom.set('height', str(line_height))
            line_geom.set('as', 'geometry')
        
        # Icon
        icon_cell = ET.SubElement(root, 'mxCell')
        icon_cell.set('id', str(cell_id))
        cell_id += 1
        icon_cell.set('value', '')
        image_ref = lang_to_icon.get(lang_name, 'https://via.placeholder.com/70')
        icon_cell.set('style', f'shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;verticalAlign=top;aspect=fixed;imageAspect=0;image={image_ref};')
        icon_cell.set('vertex', '1')
        icon_cell.set('parent', '1')
        icon_geom = ET.SubElement(icon_cell, 'mxGeometry')
        icon_geom.set('x', str(icon_x))
        icon_geom.set('y', str(icon_y))
        icon_geom.set('width', str(icon_size))
        icon_geom.set('height', str(icon_size))
        icon_geom.set('as', 'geometry')
        
        # Name label below icon
        name_cell = ET.SubElement(root, 'mxCell')
        name_cell.set('id', str(cell_id))
        cell_id += 1
        name_cell.set('value', lang_name)
        name_cell.set('style', 'text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=top;whiteSpace=wrap;fontSize=14;fontColor=#333333;fontStyle=0')
        name_cell.set('vertex', '1')
        name_cell.set('parent', '1')
        name_geom = ET.SubElement(name_cell, 'mxGeometry')
        name_geom.set('x', str(tick_x - 50))
        name_geom.set('y', str(icon_y + icon_size + 3))
        name_geom.set('width', '100')
        name_geom.set('height', str(name_height))
        name_geom.set('as', 'geometry')
    
    return model

def encode_model_for_diagram(model):
    """Encode mxGraphModel for inclusion in diagram element."""
    model_xml = ET.tostring(model, encoding='unicode')
    # URL encode
    encoded = urllib.parse.quote(model_xml, safe='')
    # Compress with deflate
    compressed = zlib.compress(encoded.encode('utf-8'), 9)
    deflated = compressed[2:-4]  # Remove zlib header/trailer
    # Base64 encode
    b64 = base64.b64encode(deflated).decode('ascii')
    return b64

def create_mxfile(model, diagram_name="language-history"):
    """Create complete mxfile structure."""
    mxfile = ET.Element('mxfile')
    mxfile.set('host', 'Electron')
    mxfile.set('modified', '2024-01-01T00:00:00.000Z')
    mxfile.set('agent', 'Python rebuild script')
    mxfile.set('version', '26.0.7')
    mxfile.set('type', 'device')
    
    diagram = ET.SubElement(mxfile, 'diagram')
    diagram.set('id', 'timeline-diagram-1')
    diagram.set('name', diagram_name)
    
    # Encode and set diagram content
    encoded_model = encode_model_for_diagram(model)
    diagram.text = encoded_model
    
    return mxfile

def main():
    if len(sys.argv) < 3:
        print("Usage: python rebuild_timeline.py <input.drawio.svg> <output.drawio>")
        sys.exit(1)
    
    input_svg = sys.argv[1]
    output_drawio = sys.argv[2]
    
    print(f"Processing {input_svg}...")
    
    # Extract existing content
    try:
        mxfile_xml, was_compressed = extract_mxfile_content(input_svg)
        print(f"Extracted mxfile (compressed: {was_compressed})")
        
        model = parse_mxfile(mxfile_xml)
        print("Parsed mxGraphModel")
        
        old_icons = extract_icon_images(model)
        print(f"Found {len(old_icons)} icon images")
        
    except Exception as e:
        print(f"Warning: Could not extract old icons: {e}")
        print("Proceeding with placeholder images...")
        old_icons = {}
    
    # Build new model
    new_model = build_new_model(old_icons)
    print("Built new model")
    
    # Create mxfile
    mxfile = create_mxfile(new_model)
    
    # Write as .drawio file
    tree = ET.ElementTree(mxfile)
    ET.indent(tree, space='  ')
    tree.write(output_drawio, encoding='utf-8', xml_declaration=True)
    print(f"Saved to {output_drawio}")
    
    print("\nNext: Export to SVG with draw.io CLI")
    print(f"  drawio --export --format svg --embed-diagram --output <output.svg> {output_drawio}")

if __name__ == '__main__':
    main()
