#!/usr/bin/env python3
"""
Debug OCR spatial parsing
"""

import sys
from pathlib import Path
import easyocr

def debug_ocr(image_path):
    """Debug OCR extraction to see spatial layout"""
    print(f"Debugging OCR on: {image_path}")
    print("=" * 80)
    
    reader = easyocr.Reader(['en'], gpu=False)
    results = reader.readtext(image_path)
    
    print(f"\nTotal text boxes detected: {len(results)}\n")
    
    # Show first 20 boxes with positions
    for i, (bbox, text, conf) in enumerate(results[:20]):
        x_coords = [p[0] for p in bbox]
        y_coords = [p[1] for p in bbox]
        
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        x_center = (x_min + x_max) / 2
        y_center = (y_min + y_max) / 2
        
        print(f"{i:3d}: y={y_center:6.1f} x={x_center:6.1f} | '{text}'")
    
    # Group by y position
    print("\n" + "=" * 80)
    print("GROUPING BY Y-POSITION (threshold=20px):")
    print("=" * 80)
    
    text_boxes = []
    for bbox, text, conf in results:
        x_coords = [p[0] for p in bbox]
        y_coords = [p[1] for p in bbox]
        x_center = (min(x_coords) + max(x_coords)) / 2
        y_center = (min(y_coords) + max(y_coords)) / 2
        text_boxes.append({'text': text, 'x': x_center, 'y': y_center})
    
    # Sort by y
    text_boxes.sort(key=lambda b: b['y'])
    
    # Group into rows
    rows = []
    if text_boxes:
        current_row = [text_boxes[0]]
        current_y = text_boxes[0]['y']
        
        for box in text_boxes[1:]:
            if abs(box['y'] - current_y) < 20:
                current_row.append(box)
            else:
                current_row.sort(key=lambda b: b['x'])
                rows.append(current_row)
                current_row = [box]
                current_y = box['y']
        
        if current_row:
            current_row.sort(key=lambda b: b['x'])
            rows.append(current_row)
    
    print(f"\nDetected {len(rows)} rows:\n")
    for i, row in enumerate(rows[:10]):
        texts = [b['text'] for b in row]
        print(f"Row {i} ({len(texts)} cells): {texts}")

if __name__ == "__main__":
    test_image = "/home/predaopenclaw/.openclaw/media/inbound/file_4---376f9706-3cf7-498d-ba5f-bf7caedb2226.jpg"
    
    if Path(test_image).exists():
        debug_ocr(test_image)
    else:
        print(f"Image not found: {test_image}")
        sys.exit(1)
