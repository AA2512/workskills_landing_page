#!/usr/bin/env python3
"""
Script to extract SVG elements from HTML and replace them with img tags.
"""

import re
import os
from pathlib import Path

def extract_svgs_from_html(html_file_path):
    """Extract all SVG elements from HTML file and replace with img tags."""
    
    # Create svgs directory if it doesn't exist
    svgs_dir = Path("svgs")
    svgs_dir.mkdir(exist_ok=True)
    
    # Read the HTML file
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # Find all SVG elements using regex
    svg_pattern = r'(<svg[^>]*>.*?</svg>)'
    svg_matches = re.findall(svg_pattern, html_content, re.DOTALL)
    
    print(f"Found {len(svg_matches)} SVG elements")
    
    # Process each SVG
    for i, svg_content in enumerate(svg_matches):
        # Generate filename
        svg_filename = f"svg_{i+1:03d}.svg"
        svg_filepath = svgs_dir / svg_filename
        
        # Extract id attribute if it exists for better naming
        id_match = re.search(r'id="([^"]*)"', svg_content)
        if id_match:
            svg_id = id_match.group(1)
            # Clean the ID to make it a valid filename
            clean_id = re.sub(r'[^\w\-_]', '_', svg_id)
            svg_filename = f"{clean_id}.svg"
            svg_filepath = svgs_dir / svg_filename
        
        # Write SVG to file
        with open(svg_filepath, 'w', encoding='utf-8') as svg_file:
            svg_file.write(svg_content)
        
        # Extract width and height attributes for the img tag
        width_match = re.search(r'width="([^"]*)"', svg_content)
        height_match = re.search(r'height="([^"]*)"', svg_content)
        
        # Build img tag attributes
        img_attrs = f'src="svgs/{svg_filename}"'
        if width_match:
            img_attrs += f' width="{width_match.group(1)}"'
        if height_match:
            img_attrs += f' height="{height_match.group(1)}"'
        
        # Extract class attribute if it exists
        class_match = re.search(r'class="([^"]*)"', svg_content)
        if class_match:
            img_attrs += f' class="{class_match.group(1)}"'
        
        # Extract id attribute if it exists
        if id_match:
            img_attrs += f' id="{id_match.group(1)}"'
        
        # Create img tag
        img_tag = f'<img {img_attrs} alt="{svg_filename.replace(".svg", "")}" />'
        
        # Replace SVG with img tag in HTML content
        html_content = html_content.replace(svg_content, img_tag, 1)
        
        print(f"Extracted: {svg_filename}")
    
    # Write the updated HTML back to file
    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(html_content)
    
    print(f"\nCompleted! Extracted {len(svg_matches)} SVGs to 'svgs/' folder")
    print(f"Updated {html_file_path} with img tags")

if __name__ == "__main__":
    extract_svgs_from_html("index.html") 