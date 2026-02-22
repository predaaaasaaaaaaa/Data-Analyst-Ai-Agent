#!/usr/bin/env python3
"""
Test the complete data analysis pipeline end-to-end
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

import config
from src.image_processor import ImageProcessor
from src.data_analyzer import DataAnalyzer
from src.excel_generator import ExcelReportGenerator

def test_full_pipeline(image_path):
    """Test complete pipeline: OCR → Analysis → Excel"""
    print("=" * 80)
    print("TESTING COMPLETE DATA ANALYST PIPELINE")
    print("=" * 80)
    
    # Step 1: OCR Extraction
    print("\n📸 Step 1: Extracting data from image...")
    processor = ImageProcessor()
    df = processor.extract_data_from_image(image_path)
    
    if df is None or len(df) == 0:
        print("❌ FAILED - No data extracted")
        return False
    
    print(f"✅ Extracted: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"\nColumns: {list(df.columns)}")
    print(f"\nFirst 3 rows:\n{df.head(3)}")
    
    # Step 2: Data Analysis
    print("\n📊 Step 2: Analyzing data...")
    analyzer = DataAnalyzer()
    analysis = analyzer.analyze_data(df)
    
    if 'error' in analysis:
        print(f"❌ FAILED - Analysis error: {analysis['error']}")
        return False
    
    print(f"✅ Analysis complete")
    print(f"\nOverview: {analysis.get('overview', {})}")
    print(f"\nData Quality:")
    quality = analysis.get('data_quality', {})
    print(f"  - Missing values: {sum(quality.get('missing_values', {}).values())} total")
    print(f"  - Duplicates: {quality.get('duplicate_rows', 0)} rows")
    
    insights = analysis.get('insights', {}).get('insights', [])
    print(f"\n💡 Insights ({len(insights)} total):")
    for i, insight in enumerate(insights[:3], 1):
        print(f"  {i}. {insight}")
    
    # Step 3: Excel Generation
    print("\n📝 Step 3: Generating Excel report...")
    report_path = config.REPORTS_DIR / "test_analysis.xlsx"
    generator = ExcelReportGenerator()
    excel_path = generator.generate_report(df, analysis, str(report_path))
    
    if not excel_path or not Path(excel_path).exists():
        print("❌ FAILED - Excel generation failed")
        return False
    
    print(f"✅ Excel generated: {excel_path}")
    print(f"   File size: {Path(excel_path).stat().st_size / 1024:.1f} KB")
    
    # Final summary
    print("\n" + "=" * 80)
    print("✅ COMPLETE PIPELINE TEST PASSED")
    print("=" * 80)
    print(f"\n🎯 Result: Professional data analysis ready")
    print(f"   - {df.shape[0]} rows analyzed")
    print(f"   - {df.shape[1]} columns detected")
    print(f"   - {len(insights)} insights generated")
    print(f"   - Excel report: {excel_path}")
    
    return True

if __name__ == "__main__":
    # Test with the actual image from Samy's test
    test_image = "/home/predaopenclaw/.openclaw/media/inbound/file_4---376f9706-3cf7-498d-ba5f-bf7caedb2226.jpg"
    
    if Path(test_image).exists():
        success = test_full_pipeline(test_image)
        sys.exit(0 if success else 1)
    else:
        print(f"Image not found: {test_image}")
        sys.exit(1)
