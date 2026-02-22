#!/usr/bin/env python3
"""
Test OCR extraction with actual image
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.image_processor import ImageProcessor

def test_ocr(image_path):
    """Test OCR extraction"""
    print(f"Testing OCR on: {image_path}")
    print("=" * 60)
    
    processor = ImageProcessor()
    df = processor.extract_data_from_image(image_path)
    
    if df is None:
        print("❌ FAILED - No data extracted")
        return False
    
    print(f"✅ SUCCESS - Extracted table:")
    print(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    print("\nColumns:", list(df.columns))
    print("\nFirst 10 rows:")
    print(df.head(10))
    print("\nData types:")
    print(df.dtypes)
    
    return True

if __name__ == "__main__":
    # Test with the actual image from Telegram
    test_image = "/home/predaopenclaw/.openclaw/media/inbound/file_4---376f9706-3cf7-498d-ba5f-bf7caedb2226.jpg"
    
    if Path(test_image).exists():
        test_ocr(test_image)
    else:
        print(f"Image not found: {test_image}")
        sys.exit(1)
