#!/usr/bin/env python3
"""Extract and analyze the mxGraphModel from draw.io SVG files."""

import xml.etree.ElementTree as ET
import urllib.parse
import base64
import zlib
import sys

def extract_and_save_model(svg_path, output_path):
    """Extract the mxfile from SVG and save it as standalone XML."""
    tree = ET.parse(svg_path)
    root = tree.getroot()
    content = root.get('content')
    
    if not content:
        print("No content attribute found")
        return False
    
    # The content is the mxfile XML directly (uncompressed in Erstsemester)
    # or base64+deflate compressed (in PT1)
    
    # Try to detect format
    if content.startswith('<mxfile'):
        # Uncompressed
        mxfile_xml = content
        compressed = False
    else:
        # Try base64+deflate decompression
        try:
            # The format appears to be base64 encoded deflate-compressed data
            decoded = base64.b64decode(content)
            decompressed = zlib.decompress(decoded, -zlib.MAX_WBITS)
            mxfile_xml = decompressed.decode('utf-8')
            compressed = True
        except Exception as e:
            print(f"Failed to decompress: {e}")
            # Try as URL-encoded
            mxfile_xml = urllib.parse.unquote(content)
            compressed = False
    
    # Parse and pretty-print
    try:
        mxfile_tree = ET.fromstring(mxfile_xml)
        # Write with indentation
        ET.indent(mxfile_tree, space='  ')
        with open(output_path, 'w') as f:
            f.write(ET.tostring(mxfile_tree, encoding='unicode'))
        print(f"Extracted model to {output_path}")
        print(f"Compression: {'yes' if compressed else 'no'}")
        
        # Print some stats
        diagram = mxfile_tree.find('.//diagram')
        if diagram:
            model = ET.fromstring(diagram.text) if diagram.text else None
            if model:
                cells = model.findall('.//mxCell')
                print(f"Found {len(cells)} cells in the diagram")
                
                # Find image cells
                image_cells = [c for c in cells if 'image' in c.get('style', '').lower()]
                print(f"Found {len(image_cells)} image cells")
                
                for i, cell in enumerate(image_cells[:5]):  # Show first 5
                    print(f"\nImage cell {i+1}:")
                    print(f"  ID: {cell.get('id')}")
                    print(f"  Value: {cell.get('value', '')[:50]}")
                    style = cell.get('style', '')
                    if 'image=' in style:
                        img_start = style.find('image=')
                        img_part = style[img_start:img_start+100]
                        print(f"  Image ref: {img_part}")
        
        return True
    except Exception as e:
        print(f"Failed to parse mxfile: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python extract_model.py <input.drawio.svg> <output.xml>")
        sys.exit(1)
    
    extract_and_save_model(sys.argv[1], sys.argv[2])
