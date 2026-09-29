#!/usr/bin/env python3
"""
Corrected rebuild with proper icon mappings and fixes for:
1. Icons matched to correct languages (using year proximity from original)
2. html=0 in text styles to prevent "Text is not SVG" foreignObject fallback
3. Preserved aspect ratios for icons
"""

import xml.etree.ElementTree as ET
import base64
import zlib
import urllib.parse
import json
import sys
from pathlib import Path

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

CANVAS_WIDTH = 1400
CANVAS_HEIGHT = 750
AXIS_Y = 680
MARGIN_LEFT = 60
MARGIN_RIGHT = 60

def load_icon_mappings(json_path):
    """Load icon mappings from the identification script output."""
    with open(json_path) as f:
        mappings = json.load(f)
    
    # Build language -> icon_ref dictionary
    lang_to_icon = {}
    for m in mappings:
        lang = m['language']
        # Handle duplicates (e.g., JavaScript appears twice at 1996)
        if lang not in lang_to_icon:
            lang_to_icon[lang] = {
                'image_ref': m['image_ref'],
                'width': m['icon_width'],
                'height': m['icon_height']
            }
    
    return lang_to_icon

def build_new_model(lang_to_icon):
    """Build mxGraphModel with correct mappings and fixed styles."""
    
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
    
    cell0 = ET.SubElement(root, 'mxCell')
    cell0.set('id', '0')
    
    cell1 = ET.SubElement(root, 'mxCell')
    cell1.set('id', '1')
    cell1.set('parent', '0')
    
    usable_width = CANVAS_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
    slot_width = usable_width / len(YEARS)
    
    cell_id = 100
    
    # Axis line
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
    
    # Year ticks and labels
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
        
        # Year label - FIX: html=0 to avoid foreignObject
        year_cell = ET.SubElement(root, 'mxCell')
        year_cell.set('id', str(cell_id))
        cell_id += 1
        year_cell.set('value', str(year))
        year_cell.set('style', 'text;html=0;strokeColor=none;fillColor=none;align=center;verticalAlign=top;whiteSpace=wrap;fontSize=12;fontColor=#CC0000;fontStyle=0')
        year_cell.set('vertex', '1')
        year_cell.set('parent', '1')
        year_geom = ET.SubElement(year_cell, 'mxGeometry')
        year_geom.set('x', str(tick_x - 22))
        year_geom.set('y', str(AXIS_Y + 12))
        year_geom.set('width', '44')
        year_geom.set('height', '20')
        year_geom.set('as', 'geometry')
    
    # Layout languages
    base_icon_size = 65
    name_height = 22
    gap_below_name = 8
    
    row_heights = [80, 220, 360]
    
    for idx, (lang_name, year) in enumerate(LANGUAGES):
        year_idx = YEARS.index(year)
        tick_x = MARGIN_LEFT + year_idx * slot_width
        
        # Row assignment
        if year == 1996:
            row = 0 if lang_name == 'Java' else 1
        else:
            row = idx % 3
        
        icon_y = row_heights[row]
        
        # Get icon info
        icon_info = lang_to_icon.get(lang_name, {})
        image_ref = icon_info.get('image_ref', 'https://via.placeholder.com/65')
        orig_width = icon_info.get('width', base_icon_size)
        orig_height = icon_info.get('height', base_icon_size)
        
        # FIX: Preserve aspect ratio
        aspect_ratio = orig_width / orig_height if orig_height > 0 else 1.0
        
        if aspect_ratio > 1:
            # Wider than tall
            icon_width = base_icon_size
            icon_height = base_icon_size / aspect_ratio
        else:
            # Taller than wide or square
            icon_height = base_icon_size
            icon_width = base_icon_size * aspect_ratio
        
        icon_x = tick_x - icon_width / 2
        
        # Vertical line
        line_top_y = icon_y + icon_height + name_height + gap_below_name
        line_height = AXIS_Y - line_top_y
        
        if line_height > 5:
            line_cell = ET.SubElement(root, 'mxCell')
            line_cell.set('id', str(cell_id))
            cell_id += 1
            line_cell.set('value', '')
            line_cell.set('style', 'shape=line;strokeWidth=1;strokeColor=#CC0000;direction=south;')
            line_cell.set('vertex', '1')
            line_cell.set('parent', '1')
            line_geom = ET.SubElement(line_cell, 'mxGeometry')
            line_geom.set('x', str(tick_x))
            line_geom.set('y', str(line_top_y))
            line_geom.set('width', '1')
            line_geom.set('height', str(line_height))
            line_geom.set('as', 'geometry')
        
        # Icon
        icon_cell = ET.SubElement(root, 'mxCell')
        icon_cell.set('id', str(cell_id))
        cell_id += 1
        icon_cell.set('value', '')
        icon_cell.set('style', f'shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;verticalAlign=top;aspect=fixed;imageAspect=0;image={image_ref};')
        icon_cell.set('vertex', '1')
        icon_cell.set('parent', '1')
        icon_geom = ET.SubElement(icon_cell, 'mxGeometry')
        icon_geom.set('x', str(icon_x))
        icon_geom.set('y', str(icon_y))
        icon_geom.set('width', str(icon_width))
        icon_geom.set('height', str(icon_height))
        icon_geom.set('as', 'geometry')
        
        # Name label - FIX: html=0
        name_cell = ET.SubElement(root, 'mxCell')
        name_cell.set('id', str(cell_id))
        cell_id += 1
        name_cell.set('value', lang_name)
        name_cell.set('style', 'text;html=0;strokeColor=none;fillColor=none;align=center;verticalAlign=top;whiteSpace=wrap;fontSize=14;fontColor=#333333;fontStyle=0')
        name_cell.set('vertex', '1')
        name_cell.set('parent', '1')
        name_geom = ET.SubElement(name_cell, 'mxGeometry')
        name_geom.set('x', str(tick_x - 50))
        name_geom.set('y', str(icon_y + icon_height + 2))
        name_geom.set('width', '100')
        name_geom.set('height', str(name_height))
        name_geom.set('as', 'geometry')
    
    return model

def encode_model_for_diagram(model):
    """Encode mxGraphModel for diagram element."""
    model_xml = ET.tostring(model, encoding='unicode')
    encoded = urllib.parse.quote(model_xml, safe='')
    compressed = zlib.compress(encoded.encode('utf-8'), 9)
    deflated = compressed[2:-4]
    b64 = base64.b64encode(deflated).decode('ascii')
    return b64

def create_mxfile(model):
    """Create mxfile structure."""
    mxfile = ET.Element('mxfile')
    mxfile.set('host', 'Electron')
    mxfile.set('modified', '2024-09-29T00:00:00.000Z')
    mxfile.set('agent', 'Python rebuild script v2')
    mxfile.set('version', '26.0.7')
    mxfile.set('type', 'device')
    
    diagram = ET.SubElement(mxfile, 'diagram')
    diagram.set('id', 'language-history-timeline')
    diagram.set('name', 'Language History')
    
    encoded_model = encode_model_for_diagram(model)
    diagram.text = encoded_model
    
    return mxfile

def main():
    if len(sys.argv) < 3:
        print("Usage: python rebuild_corrected.py <icon_mappings.json> <output.drawio>")
        sys.exit(1)
    
    mappings_json = sys.argv[1]
    output_drawio = sys.argv[2]
    
    print(f"Loading icon mappings from {mappings_json}...")
    lang_to_icon = load_icon_mappings(mappings_json)
    print(f"Loaded {len(lang_to_icon)} icon mappings")
    
    print("Building new model with corrected mappings...")
    new_model = build_new_model(lang_to_icon)
    print("Built model")
    
    mxfile = create_mxfile(new_model)
    
    tree = ET.ElementTree(mxfile)
    ET.indent(tree, space='  ')
    tree.write(output_drawio, encoding='utf-8', xml_declaration=True)
    print(f"Saved to {output_drawio}")

if __name__ == '__main__':
    main()
