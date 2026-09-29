#!/usr/bin/env python3
"""
Final version: Rebuild language timeline with correct icon mappings.
Based on analysis of the original files and visual layout.
"""

import xml.etree.ElementTree as ET
import base64
import zlib
import urllib.parse
import sys
import json

# Language data in chronological order
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
    
    # Check if mxGraphModel is directly a child of diagram (uncompressed format)
    model = diagram.find('mxGraphModel')
    if model is not None:
        return model
    
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

def load_icon_mappings(json_path):
    """Load the extracted icon mappings from JSON."""
    with open(json_path) as f:
        return json.load(f)

def map_icons_to_languages(icons):
    """
    Map extracted icons to languages based on the original layout.
    Looking at the original files (from user's images):
    - Row 1 (y=0): ASM, Fortran, Smalltalk, C, Java, C#, Rust (7 icons)
    - Row 2 (y=200): Simula, BASIC, C++, JavaScript, Swift (5 icons)
    - Row 3 (y=400): Objective-C, Eiffel, Python, Kotlin (4 icons)
    - Row 4 (y=600): Haskell, Ruby, Scala (3 icons)
    """
    
    # Sort by position
    icons.sort(key=lambda i: (i['y'], i['x']))
    
    # Based on the layout in the before images
    # Row 1 (y~0): 7 icons
    # Row 2 (y~200): 5 icons
    # Row 3 (y~400): 4 icons
    # Row 4 (y~600): 3 icons
    
    # Manual mapping based on visual inspection of provided images
    # This is the order they appear left-to-right, top-to-bottom
    visual_order = [
        'ASM',       # Row 1
        'Fortran',
        'Smalltalk',
        'C',
        'Java',
        'C#',
        'Rust',
        'Simula',    # Row 2
        'BASIC',
        'C++',
        'JavaScript',
        'Swift',
        'Objective-C', # Row 3
        'Eiffel',
        'Python',
        'Kotlin',
        'Haskell',   # Row 4
        'Ruby',
        'Scala',
    ]
    
    # Create mapping
    lang_to_icon = {}
    for i, lang_name in enumerate(visual_order):
        if i < len(icons):
            lang_to_icon[lang_name] = icons[i]['image_ref']
    
    return lang_to_icon

def build_new_model(lang_to_icon):
    """Build a completely new mxGraphModel with proper timeline layout."""
    
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
    
    # Base cells
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
        year_geom.set('x', str(tick_x - 22))
        year_geom.set('y', str(AXIS_Y + 12))
        year_geom.set('width', '44')
        year_geom.set('height', '20')
        year_geom.set('as', 'geometry')
    
    # Layout languages
    icon_size = 65
    name_height = 22
    gap_below_name = 8
    
    # Row heights (staggered to avoid overlap)
    row_heights = [80, 220, 360]
    
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
        
        # Vertical line from axis up to bottom of name label
        line_top_y = icon_y + icon_size + name_height + gap_below_name
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
        
        # Get icon image reference
        image_ref = lang_to_icon.get(lang_name, 'https://via.placeholder.com/65')
        
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
        name_geom.set('y', str(icon_y + icon_size + 2))
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
    deflated = compressed[2:-4]
    # Base64 encode
    b64 = base64.b64encode(deflated).decode('ascii')
    return b64

def create_mxfile(model):
    """Create complete mxfile structure."""
    mxfile = ET.Element('mxfile')
    mxfile.set('host', 'Electron')
    mxfile.set('modified', '2024-09-29T00:00:00.000Z')
    mxfile.set('agent', 'Python rebuild script')
    mxfile.set('version', '26.0.7')
    mxfile.set('type', 'device')
    
    diagram = ET.SubElement(mxfile, 'diagram')
    diagram.set('id', 'language-history-timeline')
    diagram.set('name', 'Language History')
    
    # Encode and set diagram content
    encoded_model = encode_model_for_diagram(model)
    diagram.text = encoded_model
    
    return mxfile

def main():
    if len(sys.argv) < 4:
        print("Usage: python rebuild_final.py <input.drawio.svg> <icons.json> <output.drawio>")
        sys.exit(1)
    
    input_svg = sys.argv[1]
    icons_json = sys.argv[2]
    output_drawio = sys.argv[3]
    
    print(f"Processing {input_svg}...")
    
    # Load icon mappings
    icons = load_icon_mappings(icons_json)
    print(f"Loaded {len(icons)} icons from JSON")
    
    # Map to languages
    lang_to_icon = map_icons_to_languages(icons)
    print(f"Mapped {len(lang_to_icon)} icons to languages")
    
    # Build new model
    new_model = build_new_model(lang_to_icon)
    print("Built new model")
    
    # Create mxfile
    mxfile = create_mxfile(new_model)
    
    # Write as .drawio file
    tree = ET.ElementTree(mxfile)
    ET.indent(tree, space='  ')
    tree.write(output_drawio, encoding='utf-8', xml_declaration=True)
    print(f"Saved to {output_drawio}")

if __name__ == '__main__':
    main()
