#!/usr/bin/env python3
"""Test Excel generation module independently"""

import sys
import pandas as pd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.excel_generator import ExcelReportGenerator

# Create reports dir if needed
REPORTS_DIR = Path(__file__).parent / 'data' / 'reports'
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Sample data and analysis
df = pd.DataFrame({
    'Date': ['26/02/2017', '06/02/2017', '27/01/2017'],
    'Type': ['Facture', 'Avoir', 'Devis'],
    'Amount': [673.46, 567.66, 673.46]
})

analysis = {
    'overview': {'total_rows': 3, 'total_columns': 3},
    'descriptive_stats': {'Amount': {'mean': 638.19, 'median': 673.46}},
    'data_quality': {'duplicate_rows': 0},
    'correlations': {'note': 'Not enough columns'},
    'outliers': {'note': 'No outliers detected'},
    'insights': {'insights': ['Test insight']}
}

print("Testing Excel Generator")
print("=" * 60)

generator = ExcelReportGenerator()
output_path = REPORTS_DIR / "test_excel_output.xlsx"

excel_path = generator.generate_report(df, analysis, str(output_path))

if excel_path and Path(excel_path).exists():
    size = Path(excel_path).stat().st_size / 1024
    print(f"\n✅ Excel generated: {excel_path}")
    print(f"   File size: {size:.1f} KB")
else:
    print("\n❌ Excel generation failed")
    sys.exit(1)
