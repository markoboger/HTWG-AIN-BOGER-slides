#!/usr/bin/env python3
"""
Edit draw.io SVG files to create a proper timeline layout with languages.
Processes the embedded mxGraphModel, regenerates layout, then exports with draw.io CLI.
"""

import xml.etree.ElementTree as ET
import base64
import zlib
import urllib.parse
import sys
import os
from pathlib import Path

# Language data: name -> year
LANGUAGES = {
    'ASM': 1947,
    'Fortran': 1957,
    'Simula': 1962,
    'BASIC': 1963,
    'Smalltalk': 1969,
    'C': 1978,
    'Objective-C': 1984,
    'C++': 1985,
    'Eiffel': 1986,
    'Haskell': 1990,
    'Python': 1991,
    'Ruby': 1995,
    'Java': 1996,
    'JavaScript': 1996,
    'C#': 2000,
    'Scala': 2003,
    'Kotlin': 2011,
    'Swift': 2014,
    'Rust': 2015,
}

# Get unique sorted years
YEARS = sorted(set(LANGUAGES.values()))

# Canvas dimensions
CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 700
AXIS_Y = 650  # Position of the axis line from top
MARGIN_LEFT = 50
MARGIN_RIGHT = 50

def extract_mxgraph_model(svg_path):
    """Extract the mxGraphModel from the draw.io SVG file."""
    tree = ET.parse(svg_path)
    root = tree.getroot()
    
    # Find the content attribute in the svg element
    # It contains the compressed or uncompressed mxfile
    content = root.get('content')
    
    if content:
        # Try to decode - could be URL-encoded, base64, or compressed
        try:
            # URL decode
            decoded = urllib.parse.unquote(content)
            
            # Check if it's compressed (starts with specific markers)
            if decoded.startswith('<?xml'):
                # Uncompressed
                mxfile_tree = ET.fromstring(decoded)
            else:
                # Try base64 + zlib decompression
                try:
                    compressed = base64.b64decode(decoded)
                    decompressed = zlib.decompress(compressed, -zlib.MAX_WBITS)
                    mxfile_tree = ET.fromstring(decompressed)
                except:
                    # Just try to parse as-is
                    mxfile_tree = ET.fromstring(decoded)
            
            return mxfile_tree
        except Exception as e:
            print(f"Error extracting model: {e}")
            return None
    
    return None

def find_icon_cells(diagram_elem):
    """Find all cells that represent language icons in the diagram."""
    icons = {}
    
    # Look through all mxCell elements
    for cell in diagram_elem.findall('.//mxCell'):
        value = cell.get('value', '')
        style = cell.get('style', '')
        
        # Language names might be in value or we look for image cells
        if 'image;' in style or 'shape=image' in style:
            # This is likely an icon
            cell_id = cell.get('id')
            icons[cell_id] = {
                'cell': cell,
                'value': value,
                'style': style
            }
    
    return icons

def get_icon_dimensions(cell):
    """Extract width and height from mxGeometry."""
    geom = cell.find('mxGeometry')
    if geom is not None:
        width = float(geom.get('width', 100))
        height = float(geom.get('height', 100))
        return width, height
    return 100, 100

def rebuild_diagram(mxfile_tree, is_compressed):
    """Rebuild the entire diagram with proper timeline layout."""
    
    # Find the diagram element
    diagram = mxfile_tree.find('.//diagram')
    if diagram is None:
        print("No diagram element found")
        return None
    
    # Get or create mxGraphModel
    graph_model = diagram.find('mxGraphModel')
    if graph_model is None:
        print("No mxGraphModel found")
        return None
    
    # Get root element
    root = graph_model.find('root')
    if root is None:
        root = ET.SubElement(graph_model, 'root')
    
    # Clear all existing cells except the base cells (layer 0 and 1)
    base_cells = []
    for cell in list(root):
        cell_id = cell.get('id')
        if cell_id in ('0', '1'):
            base_cells.append(cell)
    
    root.clear()
    for cell in base_cells:
        root.append(cell)
    
    # Calculate layout
    usable_width = CANVAS_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
    slot_width = usable_width / len(YEARS)
    
    # Determine icon scale to fit in slots
    max_icon_width = slot_width * 0.9
    icon_scale = 0.6  # Start with this, we'll adjust per icon
    
    # Add axis line
    axis_cell_id = 'axis_line_1'
    axis_cell = ET.SubElement(root, 'mxCell')
    axis_cell.set('id', axis_cell_id)
    axis_cell.set('value', '')
    axis_cell.set('style', 'shape=line;strokeColor=#CC0000;strokeWidth=2;')
    axis_cell.set('parent', '1')
    axis_cell.set('vertex', '1')
    axis_geom = ET.SubElement(axis_cell, 'mxGeometry')
    axis_geom.set('x', str(MARGIN_LEFT))
    axis_geom.set('y', str(AXIS_Y))
    axis_geom.set('width', str(usable_width))
    axis_geom.set('height', '1')
    axis_geom.set('as', 'geometry')
    
    # Add year ticks and labels
    cell_counter = 100
    for i, year in enumerate(YEARS):
        tick_x = MARGIN_LEFT + i * slot_width
        
        # Tick mark (small vertical line)
        tick_cell = ET.SubElement(root, 'mxCell')
        tick_cell.set('id', f'tick_{cell_counter}')
        tick_cell.set('value', '')
        tick_cell.set('style', 'shape=line;strokeColor=#CC0000;strokeWidth=2;direction=south;')
        tick_cell.set('parent', '1')
        tick_cell.set('vertex', '1')
        tick_geom = ET.SubElement(tick_cell, 'mxGeometry')
        tick_geom.set('x', str(tick_x))
        tick_geom.set('y', str(AXIS_Y))
        tick_geom.set('width', '1')
        tick_geom.set('height', '10')
        tick_geom.set('as', 'geometry')
        cell_counter += 1
        
        # Year label
        year_label = ET.SubElement(root, 'mxCell')
        year_label.set('id', f'year_{cell_counter}')
        year_label.set('value', str(year))
        year_label.set('style', 'text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=top;whiteSpace=wrap;fontSize=12;fontColor=#CC0000;')
        year_label.set('parent', '1')
        year_label.set('vertex', '1')
        year_geom = ET.SubElement(year_label, 'mxGeometry')
        year_geom.set('x', str(tick_x - 20))
        year_geom.set('y', str(AXIS_Y + 12))
        year_geom.set('width', '40')
        year_geom.set('height', '20')
        year_geom.set('as', 'geometry')
        cell_counter += 1
    
    # Group languages by year for layout
    langs_by_year = {}
    for lang, year in LANGUAGES.items():
        if year not in langs_by_year:
            langs_by_year[year] = []
        langs_by_year[year].append(lang)
    
    # Icon assets mapping (you'll need to identify these from the original files)
    # For now, we'll use placeholder references - these need to be updated with actual image data
    icon_images = {
        'ASM': 'data:image/png;base64,...',  # Placeholder
        'Fortran': 'data:image/png;base64,...',
        'Simula': 'data:image/png;base64,...',
        'BASIC': 'data:image/png;base64,...',
        'Smalltalk': 'data:image/png;base64,...',
        'C': 'data:image/png;base64,...',
        'Objective-C': 'data:image/png;base64,...',
        'C++': 'data:image/png;base64,...',
        'Eiffel': 'data:image/png;base64,...',
        'Haskell': 'data:image/png;base64,...',
        'Python': 'data:image/png;base64,...',
        'Ruby': 'data:image/png;base64,...',
        'Java': 'data:image/png;base64,...',
        'JavaScript': 'data:image/png;base64,...',
        'C#': 'data:image/png;base64,...',
        'Scala': 'data:image/png;base64,...',
        'Kotlin': 'data:image/png;base64,...',
        'Swift': 'data:image/png;base64,...',
        'Rust': 'data:image/png;base64,...',
    }
    
    # Layout languages
    icon_size = 80  # Base icon size
    name_height = 20
    line_spacing = 15
    
    # Define row heights (staggered by index mod 3)
    row_heights = [150, 300, 450]
    
    chronological_langs = sorted(LANGUAGES.items(), key=lambda x: (x[1], x[0]))
    
    for idx, (lang, year) in enumerate(chronological_langs):
        year_index = YEARS.index(year)
        tick_x = MARGIN_LEFT + year_index * slot_width
        
        # Determine row (stagger by chronological index)
        # Special handling for 1996 (Java and JavaScript)
        if year == 1996:
            if lang == 'Java':
                row = 0
            else:  # JavaScript
                row = 1
        else:
            row = idx % 3
        
        icon_y = row_heights[row]
        
        # Add vertical line from tick to icon
        line_cell = ET.SubElement(root, 'mxCell')
        line_cell.set('id', f'line_{cell_counter}')
        line_cell.set('value', '')
        line_cell.set('style', 'shape=line;strokeColor=#CC0000;strokeWidth=1;direction=south;')
        line_cell.set('parent', '1')
        line_cell.set('vertex', '1')
        line_geom = ET.SubElement(line_cell, 'mxGeometry')
        line_geom.set('x', str(tick_x))
        line_geom.set('y', str(icon_y + icon_size + name_height + line_spacing))
        line_geom.set('width', '1')
        line_geom.set('height', str(AXIS_Y - icon_y - icon_size - name_height - line_spacing))
        line_geom.set('as', 'geometry')
        cell_counter += 1
        
        # Add icon (placeholder - need actual image reference)
        icon_cell = ET.SubElement(root, 'mxCell')
        icon_cell.set('id', f'icon_{cell_counter}')
        icon_cell.set('value', '')
        icon_cell.set('style', f'shape=image;verticalLabelPosition=bottom;labelBackgroundColor=none;verticalAlign=top;aspect=fixed;imageAspect=0;image=https://via.placeholder.com/{icon_size};')
        icon_cell.set('parent', '1')
        icon_cell.set('vertex', '1')
        icon_geom = ET.SubElement(icon_cell, 'mxGeometry')
        icon_geom.set('x', str(tick_x - icon_size / 2))
        icon_geom.set('y', str(icon_y))
        icon_geom.set('width', str(icon_size))
        icon_geom.set('height', str(icon_size))
        icon_geom.set('as', 'geometry')
        cell_counter += 1
        
        # Add name label below icon
        name_cell = ET.SubElement(root, 'mxCell')
        name_cell.set('id', f'name_{cell_counter}')
        name_cell.set('value', lang)
        name_cell.set('style', 'text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=top;whiteSpace=wrap;fontSize=14;fontColor=#333333;')
        name_cell.set('parent', '1')
        name_cell.set('vertex', '1')
        name_geom = ET.SubElement(name_cell, 'mxGeometry')
        name_geom.set('x', str(tick_x - 50))
        name_geom.set('y', str(icon_y + icon_size + 5))
        name_geom.set('width', '100')
        name_geom.set('height', str(name_height))
        name_geom.set('as', 'geometry')
        cell_counter += 1
    
    return mxfile_tree

def encode_mxgraph_model(mxfile_tree, compress=False):
    """Encode the mxGraphModel back into the format needed for the SVG content attribute."""
    xml_str = ET.tostring(mxfile_tree, encoding='unicode')
    
    if compress:
        # Compress with zlib
        compressed = zlib.compress(xml_str.encode('utf-8'), 9)
        # Remove zlib header for deflate format
        deflated = compressed[2:-4]
        # Base64 encode
        encoded = base64.b64encode(deflated).decode('ascii')
    else:
        # URL encode
        encoded = urllib.parse.quote(xml_str)
    
    return encoded

def main():
    if len(sys.argv) < 2:
        print("Usage: python timeline_editor.py <input.drawio.svg> [output.drawio.svg]")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else input_path.replace('.drawio.svg', '_edited.drawio.svg')
    
    print(f"Processing {input_path}...")
    
    # Determine if file is compressed by checking file size / complexity
    file_size = os.path.getsize(input_path)
    is_compressed = file_size < 500000  # Simple heuristic
    
    # Extract model
    mxfile_tree = extract_mxgraph_model(input_path)
    if mxfile_tree is None:
        print("Failed to extract mxGraphModel")
        sys.exit(1)
    
    # Rebuild diagram
    new_tree = rebuild_diagram(mxfile_tree, is_compressed)
    if new_tree is None:
        print("Failed to rebuild diagram")
        sys.exit(1)
    
    # Encode back
    encoded_content = encode_mxgraph_model(new_tree, compress=is_compressed)
    
    # Read original SVG and update content attribute
    tree = ET.parse(input_path)
    root = tree.getroot()
    root.set('content', encoded_content)
    
    # Write output
    tree.write(output_path, encoding='utf-8', xml_declaration=True)
    print(f"Saved to {output_path}")
    print("\nNow run draw.io CLI to regenerate the visible SVG:")
    print(f"  drawio --export --format svg --embed-diagram --output {output_path} {output_path}")

if __name__ == '__main__':
    main()
