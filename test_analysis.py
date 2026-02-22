#!/usr/bin/env python3
"""Test data analysis module independently"""

import sys
import pandas as pd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.data_analyzer import DataAnalyzer

# Create sample data matching what OCR extracts
data = {
    'Date': ['26/02/2017', '06/02/2017', '27/01/2017'],
    'Type': ['Facture', 'Avoir', 'Devis'],
    'Client': ['CLI-CLI', 'ISOLDE', 'Testmail'],
    'Amount': [673.46, 567.66, 673.46]
}

df = pd.DataFrame(data)

print("Testing Data Analyzer")
print("=" * 60)
print(f"\nSample data:\n{df}\n")

analyzer = DataAnalyzer()
results = analyzer.analyze_data(df)

print("Analysis Results:")
print(f"\nOverview: {results.get('overview', {})}")
print(f"\nDescriptive Stats: {results.get('descriptive_stats', {})}")
print(f"\nData Quality: {results.get('data_quality', {})}")
print(f"\nInsights: {results.get('insights', {})}")

print("\n✅ Analysis module working")
