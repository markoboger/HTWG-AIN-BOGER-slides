#!/usr/bin/env python3
"""
Restructure language history diagrams into timeline format.
PHASE 2: Modify both draw.io diagrams.
"""
import xml.etree.ElementTree as ET
import urllib.parse
import base64
import zlib
import re
import math

# Confirmed language mapping by cell ID
LANGUAGE_MAP = {
    '3': ('ASM', 1947),
    '4': ('Fortran', 1957),
    '20': ('Simula', 1962),
    '17': ('BASIC', 1963),
    '16': ('Smalltalk', 1969),
    '5': ('C', 1978),
    '18': ('Objective-C', 1984),
    '7': ('C++', 1985),
    '21': ('Eiffel', 1986),
    '15': ('Haskell', 1990),
    '14': ('Python', 1991),
    '13': ('Ruby', 1995),
    '8': ('Java', 1996),
    '19': ('JavaScript', 1996),
    '9': ('C#', 2000),
    '22': ('Scala', 2003),
    '12': ('Kotlin', 2011),
    '11': ('Swift', 2014),
    '10': ('Rust', 2015)
}

# Timeline years (18 slots)
TIMELINE_YEARS = [1947, 1957, 1962, 1963, 1969, 1978, 1984, 1985, 1986, 
                  1990, 1991, 1995, 1996, 2000, 2003, 2011, 2014, 2015]

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 800
LEFT_MARGIN = 50
RIGHT_MARGIN = 50
TIMELINE_WIDTH = CANVAS_WIDTH - LEFT_MARGIN - RIGHT_MARGIN
AXIS_Y = 720
ICON_MAX_SIZE = 60
WORDMARK_MAX_WIDTH = 70
LABEL_HEIGHT = 20
ROW_SPACING = 180

def parse_drawio_svg(svg_path):
    """Parse draw.io SVG."""
    tree = ET.parse(svg_path)
    root = tree.getroot()
    content_attr = root.get('content')
    
    mxfile = ET.fromstring(content_attr)
    diagram = mxfile.find('diagram')
    
    model = diagram.find('mxGraphModel')
    if model is not None:
        return tree, root, mxfile, diagram, model, False
    
    # Compressed
    diagram_text = diagram.text
    compressed = base64.b64decode(diagram_text)
    decompressed = zlib.decompress(compressed, -zlib.MAX_WBITS).decode('utf-8')
    decoded = urllib.parse.unquote(decompressed)
    model = ET.fromstring(decoded)
    
    return tree, root, mxfile, diagram, model, True

def get_year_x_position(year):
    """Calculate x position for a given year."""
    if year not in TIMELINE_YEARS:
        return None
    idx = TIMELINE_YEARS.index(year)
    slot_width = TIMELINE_WIDTH / (len(TIMELINE_YEARS) - 1)
    return LEFT_MARGIN + idx * slot_width

def get_row_y_position(chronological_index):
    """Calculate y position based on chronological index (i mod 3)."""
    row = chronological_index % 3
    # Row 0 at top, row 2 at bottom
    base_y = 100
    return base_y + row * ROW_SPACING

def get_next_cell_id(model_root):
    """Get next available cell ID."""
    max_id = 0
    for cell in model_root.findall('.//mxCell'):
        cell_id = cell.get('id')
        if cell_id and cell_id.isdigit():
            max_id = max(max_id, int(cell_id))
    return str(max_id + 1)

def restructure_diagram(svg_path, output_path, is_compressed):
    """Restructure a single diagram."""
    print(f"\nProcessing: {svg_path}")
    
    # Parse
    tree, svg_root, mxfile, diagram, model, was_compressed = parse_drawio_svg(svg_path)
    model_root = model.find('root')
    
    # Track chronological order
    chrono_order = []
    for year in sorted(set(y for _, y in LANGUAGE_MAP.values())):
        for cell_id, (lang, y) in LANGUAGE_MAP.items():
            if y == year:
                chrono_order.append(cell_id)
    
    # Step 1: Reposition image cells
    print("Step 1: Repositioning icons...")
    for cell in model_root.findall('mxCell'):
        cell_id = cell.get('id')
        if cell_id in LANGUAGE_MAP:
            lang, year = LANGUAGE_MAP[cell_id]
            geom = cell.find('mxGeometry')
            if geom is not None:
                # Get original size
                orig_w = float(geom.get('width', 60))
                orig_h = float(geom.get('height', 60))
                
                # Determine max size (wordmarks get more width)
                is_wordmark = lang in ['Simula', 'Eiffel']
                max_w = WORDMARK_MAX_WIDTH if is_wordmark else ICON_MAX_SIZE
                max_h = ICON_MAX_SIZE
                
                # Scale uniformly
                scale = min(max_w / orig_w, max_h / orig_h, 1.0)
                new_w = orig_w * scale
                new_h = orig_h * scale
                
                # Calculate position
                target_x = get_year_x_position(year)
                chrono_idx = chrono_order.index(cell_id)
                
                # Special handling for 1996: Java row 0, JavaScript row 1
                if year == 1996:
                    if lang == 'Java':
                        chrono_idx_adj = chrono_order.index('8')  # Force row 0
                        row_y = get_row_y_position(0)
                    else:  # JavaScript
                        chrono_idx_adj = chrono_order.index('19')
                        row_y = get_row_y_position(1)
                else:
                    row_y = get_row_y_position(chrono_idx)
                
                # Center horizontally at target_x
                icon_x = target_x - new_w / 2
                icon_y = row_y
                
                geom.set('x', str(round(icon_x, 1)))
                geom.set('y', str(round(icon_y, 1)))
                geom.set('width', str(round(new_w, 1)))
                geom.set('height', str(round(new_h, 1)))
                
                print(f"  {cell_id:3} {lang:12} {year} -> x={round(icon_x,1):6.1f} y={round(icon_y,1):6.1f} ({round(new_w,1)}x{round(new_h,1)})")
    
    # Step 2: Delete all year text cells
    print("Step 2: Deleting original year labels...")
    cells_to_remove = []
    for cell in model_root.findall('mxCell'):
        value = cell.get('value', '')
        if value and re.search(r'\b(194\d|195\d|196\d|197\d|198\d|199\d|200\d|201\d|202\d)\b', value):
            cells_to_remove.append(cell)
    
    for cell in cells_to_remove:
        model_root.remove(cell)
        print(f"  Removed year label cell {cell.get('id')}")
    
    # Get next ID
    next_id = int(get_next_cell_id(model_root))
    
    # Step 3 & 4: Add axis, ticks, year labels, vertical lines, and name labels
    print("Step 3-4: Adding axis, ticks, labels, and lines...")
    
    # Add horizontal axis line (behind, low z-order)
    axis_id = str(next_id)
    next_id += 1
    axis_cell = ET.SubElement(model_root, 'mxCell')
    axis_cell.set('id', axis_id)
    axis_cell.set('value', '')
    axis_cell.set('style', 'endArrow=none;html=1;strokeColor=#000000;strokeWidth=2;')
    axis_cell.set('edge', '1')
    axis_cell.set('parent', '1')
    
    axis_geom = ET.SubElement(axis_cell, 'mxGeometry')
    axis_geom.set('width', '50')
    axis_geom.set('height', '50')
    axis_geom.set('relative', '1')
    axis_geom.set('as', 'geometry')
    
    axis_array = ET.SubElement(axis_geom, 'Array')
    axis_array.set('as', 'points')
    
    # Add points for axis line
    pt_start = ET.SubElement(axis_array, 'mxPoint')
    pt_start.set('x', str(LEFT_MARGIN))
    pt_start.set('y', str(AXIS_Y))
    
    pt_end = ET.SubElement(axis_array, 'mxPoint')
    pt_end.set('x', str(CANVAS_WIDTH - RIGHT_MARGIN))
    pt_end.set('y', str(AXIS_Y))
    
    # For each year slot, add tick, year label, and vertical line
    for year in TIMELINE_YEARS:
        x_pos = get_year_x_position(year)
        
        # Find icons at this year to determine max y
        icon_bottoms = []
        name_label_ys = []
        for cell_id, (lang, y) in LANGUAGE_MAP.items():
            if y == year:
                cell = model_root.find(f".//mxCell[@id='{cell_id}']")
                if cell is not None:
                    geom = cell.find('mxGeometry')
                    if geom is not None:
                        icon_y = float(geom.get('y', 0))
                        icon_h = float(geom.get('height', 60))
                        icon_bottom = icon_y + icon_h
                        icon_bottoms.append(icon_bottom)
                        name_label_ys.append(icon_bottom + LABEL_HEIGHT + 5)
        
        max_name_bottom = max(name_label_ys) if name_label_ys else AXIS_Y - 100
        
        # Vertical red line from tick to bottom of name labels
        line_id = str(next_id)
        next_id += 1
        line_cell = ET.SubElement(model_root, 'mxCell')
        line_cell.set('id', line_id)
        line_cell.set('value', '')
        line_cell.set('style', 'endArrow=none;html=1;strokeColor=#CC0000;strokeWidth=1;')
        line_cell.set('edge', '1')
        line_cell.set('parent', '1')
        
        line_geom = ET.SubElement(line_cell, 'mxGeometry')
        line_geom.set('width', '50')
        line_geom.set('height', '50')
        line_geom.set('relative', '1')
        line_geom.set('as', 'geometry')
        
        line_array = ET.SubElement(line_geom, 'Array')
        line_array.set('as', 'points')
        
        line_pt1 = ET.SubElement(line_array, 'mxPoint')
        line_pt1.set('x', str(round(x_pos, 1)))
        line_pt1.set('y', str(AXIS_Y))
        
        line_pt2 = ET.SubElement(line_array, 'mxPoint')
        line_pt2.set('x', str(round(x_pos, 1)))
        line_pt2.set('y', str(round(max_name_bottom, 1)))
        
        # Red year label below axis
        year_label_id = str(next_id)
        next_id += 1
        year_cell = ET.SubElement(model_root, 'mxCell')
        year_cell.set('id', year_label_id)
        year_cell.set('value', str(year))
        year_cell.set('style', 'text;html=0;strokeColor=none;fillColor=none;align=center;verticalAlign=top;whiteSpace=wrap;rounded=0;fontColor=#CC0000;fontSize=12;')
        year_cell.set('vertex', '1')
        year_cell.set('parent', '1')
        
        year_geom = ET.SubElement(year_cell, 'mxGeometry')
        year_geom.set('x', str(round(x_pos - 20, 1)))
        year_geom.set('y', str(AXIS_Y + 5))
        year_geom.set('width', '40')
        year_geom.set('height', '20')
        year_geom.set('as', 'geometry')
    
    # Step 3: Add name labels under each icon
    print("Step 3: Adding name labels...")
    for cell_id, (lang, year) in LANGUAGE_MAP.items():
        # Find the icon cell to get its position
        icon_cell = model_root.find(f".//mxCell[@id='{cell_id}']")
        if icon_cell is not None:
            icon_geom = icon_cell.find('mxGeometry')
            if icon_geom is not None:
                icon_x = float(icon_geom.get('x', 0))
                icon_y = float(icon_geom.get('y', 0))
                icon_w = float(icon_geom.get('width', 60))
                icon_h = float(icon_geom.get('height', 60))
                
                # Calculate label position (centered below icon)
                label_x = icon_x + icon_w / 2 - 40  # Label width = 80
                label_y = icon_y + icon_h + 5
                
                # Create name label
                label_id = str(next_id)
                next_id += 1
                label_cell = ET.SubElement(model_root, 'mxCell')
                label_cell.set('id', label_id)
                label_cell.set('value', lang)
                label_cell.set('style', 'text;html=0;strokeColor=none;fillColor=none;align=center;verticalAlign=top;whiteSpace=wrap;rounded=0;fontColor=#333333;fontSize=14;')
                label_cell.set('vertex', '1')
                label_cell.set('parent', '1')
                
                label_geom = ET.SubElement(label_cell, 'mxGeometry')
                label_geom.set('x', str(round(label_x, 1)))
                label_geom.set('y', str(round(label_y, 1)))
                label_geom.set('width', '80')
                label_geom.set('height', str(LABEL_HEIGHT))
                label_geom.set('as', 'geometry')
                
                print(f"  Added label '{lang}' below cell {cell_id}")
    
    # Save modified model
    print("Saving modified diagram...")
    
    if was_compressed:
        # Re-compress
        model_str = ET.tostring(model, encoding='unicode')
        encoded = urllib.parse.quote(model_str)
        compressed = zlib.compress(encoded.encode('utf-8'), 9)[2:-4]
        b64 = base64.b64encode(compressed).decode('ascii')
        diagram.text = b64
        # Clear children
        for child in list(diagram):
            diagram.remove(child)
    else:
        # Update uncompressed
        pass  # model already updated in place
    
    # Write back
    tree.write(output_path, encoding='utf-8', xml_declaration=True)
    print(f"Saved: {output_path}")
    
    return True

def main():
    files = [
        ('lectures/Einführung AIN/diagrams/language-history.drawio.svg', False),
        ('lectures/programmiertechnik-I/diagrams/language-history.drawio.svg', True)
    ]
    
    for svg_file, is_compressed in files:
        restructure_diagram(svg_file, svg_file, is_compressed)
    
    print("\nDiagram restructuring complete!")

if __name__ == '__main__':
    main()
