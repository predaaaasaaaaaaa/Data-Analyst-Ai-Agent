#!/usr/bin/env python3
"""
Test with realistic business data to verify human-quality insights
"""

import sys
import pandas as pd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.data_analyzer import DataAnalyzer
from src.excel_generator import ExcelReportGenerator

# Realistic sales data (company quarterly performance)
business_data = pd.DataFrame({
    'Quarter': ['Q1-2025', 'Q2-2025', 'Q3-2025', 'Q4-2025'],
    'Revenue': [125000, 148000, 152000, 189000],
    'Costs': [95000, 102000, 98000, 112000],
    'Customers': [450, 520, 580, 720],
    'Orders': [1200, 1450, 1580, 2100],
    'Avg_Order_Value': [104.17, 102.07, 96.20, 90.00]
})

print("=" * 80)
print("TESTING WITH REALISTIC BUSINESS DATA")
print("=" * 80)
print(f"\nSales Data (4 quarters):\n{business_data}\n")

# Analyze
analyzer = DataAnalyzer()
results = analyzer.analyze_data(business_data)

print("\n📊 ANALYSIS RESULTS:")
print("=" * 80)

print("\n1. BUSINESS CONTEXT:")
overview = results.get('overview', {})
print(f"   Dataset: {overview.get('total_rows')} quarters analyzed")
print(f"   Metrics tracked: {overview.get('total_columns')} KPIs")

print("\n2. TREND IDENTIFICATION:")
trends = results.get('trends', {})
for metric, trend_data in trends.items():
    if isinstance(trend_data, dict):
        direction = trend_data.get('trend', 'unknown')
        change = trend_data.get('change_percentage', 0)
        print(f"   {metric}: {direction} ({change:+.1f}%)")

print("\n3. DATA QUALITY:")
quality = results.get('data_quality', {})
missing = sum(quality.get('missing_values', {}).values())
print(f"   Missing data: {missing} values")
print(f"   Duplicates: {quality.get('duplicate_rows', 0)} records")

print("\n4. INSIGHTS & RECOMMENDATIONS:")
insights = results.get('insights', {}).get('insights', [])
for i, insight in enumerate(insights, 1):
    print(f"   {i}. {insight}")

print("\n" + "=" * 80)
print("EVALUATION: Are these insights human-quality?")
print("=" * 80)
print("\n❓ Questions to answer:")
print("   - Does it explain WHAT happened? (revenue growth)")
print("   - Does it explain WHY? (customer acquisition)")  
print("   - Does it explain IMPACT? (profitability trends)")
print("   - Does it give ACTIONS? (specific next steps)")
