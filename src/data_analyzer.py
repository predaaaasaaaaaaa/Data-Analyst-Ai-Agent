import logging
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)


class DataAnalyzer:
    def __init__(self):
        self.logger = logger
        self.analysis_results = {}

    def analyze_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Perform comprehensive data analysis
        
        Args:
            df: Input DataFrame
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            if df is None or len(df) == 0:
                self.logger.warning("Empty DataFrame provided")
                return {'error': 'No data to analyze'}
            
            self.logger.info(f"Starting analysis on {df.shape[0]} rows, {df.shape[1]} columns")
            
            # Run analyses
            self.analysis_results = {
                'overview': self._analyze_overview(df),
                'descriptive_stats': self._analyze_descriptive_stats(df),
                'data_quality': self._analyze_data_quality(df),
                'correlations': self._analyze_correlations(df),
                'outliers': self._detect_outliers(df),
                'trends': self._detect_trends(df),
                'insights': self._generate_insights(df),
            }
            
            return self.analysis_results
            
        except Exception as e:
            self.logger.error(f"Error analyzing data: {e}", exc_info=True)
            return {'error': str(e)}

    def _analyze_overview(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Basic overview of the dataset"""
        return {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'column_names': list(df.columns),
            'column_types': dict(df.dtypes),
            'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2,
        }

    def _analyze_descriptive_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate descriptive statistics"""
        numeric_df = df.select_dtypes(include=[np.number])
        
        if numeric_df.empty:
            return {'note': 'No numeric columns found'}
        
        stats = {}
        for col in numeric_df.columns:
            stats[col] = {
                'mean': float(numeric_df[col].mean()),
                'median': float(numeric_df[col].median()),
                'std': float(numeric_df[col].std()),
                'min': float(numeric_df[col].min()),
                'max': float(numeric_df[col].max()),
                'q25': float(numeric_df[col].quantile(0.25)),
                'q75': float(numeric_df[col].quantile(0.75)),
                'skewness': float(numeric_df[col].skew()),
                'kurtosis': float(numeric_df[col].kurtosis()),
            }
        
        return stats

    def _analyze_data_quality(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze data quality issues"""
        quality = {
            'missing_values': df.isnull().sum().to_dict(),
            'missing_percentage': (df.isnull().sum() / len(df) * 100).to_dict(),
            'duplicate_rows': len(df[df.duplicated()]),
            'duplicate_percentage': len(df[df.duplicated()]) / len(df) * 100,
        }
        
        # Data type analysis
        quality['data_types'] = {
            'numeric': len(df.select_dtypes(include=[np.number]).columns),
            'categorical': len(df.select_dtypes(include=['object']).columns),
            'datetime': len(df.select_dtypes(include=['datetime64']).columns),
        }
        
        return quality

    def _analyze_correlations(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze correlations between columns"""
        numeric_df = df.select_dtypes(include=[np.number])
        
        if numeric_df.shape[1] < 2:
            return {'note': 'Not enough numeric columns for correlation'}
        
        try:
            corr_matrix = numeric_df.corr()
            
            # Find strong correlations (> 0.7)
            strong_corr = {}
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    col1, col2 = corr_matrix.columns[i], corr_matrix.columns[j]
                    corr_val = corr_matrix.iloc[i, j]
                    if abs(corr_val) > 0.7:
                        strong_corr[f"{col1} <-> {col2}"] = float(corr_val)
            
            return {
                'correlation_matrix': corr_matrix.to_dict(),
                'strong_correlations': strong_corr,
            }
        except Exception as e:
            self.logger.debug(f"Correlation analysis failed: {e}")
            return {'error': str(e)}

    def _detect_outliers(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Detect outliers using IQR method"""
        numeric_df = df.select_dtypes(include=[np.number])
        
        outliers = {}
        for col in numeric_df.columns:
            Q1 = numeric_df[col].quantile(0.25)
            Q3 = numeric_df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outlier_mask = (numeric_df[col] < lower_bound) | (numeric_df[col] > upper_bound)
            outlier_count = outlier_mask.sum()
            
            if outlier_count > 0:
                outliers[col] = {
                    'count': int(outlier_count),
                    'percentage': float(outlier_count / len(df) * 100),
                    'values': numeric_df.loc[outlier_mask, col].tolist(),
                }
        
        return outliers if outliers else {'note': 'No outliers detected'}

    def _detect_trends(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Detect trends in numeric columns"""
        numeric_df = df.select_dtypes(include=[np.number])
        
        trends = {}
        for col in numeric_df.columns:
            # Simple trend: compare first half vs second half
            mid = len(numeric_df) // 2
            first_half_mean = numeric_df[col][:mid].mean()
            second_half_mean = numeric_df[col][mid:].mean()
            
            change = second_half_mean - first_half_mean
            change_percent = (change / first_half_mean * 100) if first_half_mean != 0 else 0
            
            trend = 'increasing' if change > 0 else 'decreasing'
            
            trends[col] = {
                'trend': trend,
                'change_percentage': float(change_percent),
                'first_half_avg': float(first_half_mean),
                'second_half_avg': float(second_half_mean),
            }
        
        return trends if trends else {'note': 'No trends detected'}

    def _generate_insights(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate business-focused actionable insights like a human analyst"""
        insights = []
        
        # Get trends for business analysis
        trends = self._detect_trends(df)
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Identify business metrics by common naming patterns
        revenue_cols = [c for c in numeric_cols if any(x in c.lower() for x in ['revenue', 'sales', 'income'])]
        cost_cols = [c for c in numeric_cols if any(x in c.lower() for x in ['cost', 'expense', 'spend'])]
        customer_cols = [c for c in numeric_cols if any(x in c.lower() for x in ['customer', 'user', 'client'])]
        order_cols = [c for c in numeric_cols if any(x in c.lower() for x in ['order', 'transaction', 'purchase'])]
        value_cols = [c for c in numeric_cols if any(x in c.lower() for x in ['value', 'price', 'avg', 'average'])]
        
        # BUSINESS INSIGHT 1: Revenue performance
        if revenue_cols and isinstance(trends.get(revenue_cols[0]), dict):
            rev_trend = trends[revenue_cols[0]]
            change_pct = rev_trend.get('change_percentage', 0)
            direction = rev_trend.get('trend', '')
            
            if abs(change_pct) > 10:
                # Connect to customer growth if available
                driver = ""
                if customer_cols and isinstance(trends.get(customer_cols[0]), dict):
                    cust_change = trends[customer_cols[0]].get('change_percentage', 0)
                    if cust_change > 10:
                        driver = f" driven by {cust_change:.1f}% customer growth"
                
                insights.append(
                    f"Revenue {direction} {abs(change_pct):.1f}%{driver}. "
                    f"{'Strong performance - investigate what strategies are working to replicate success.' if change_pct > 20 else 'Monitor closely and identify growth drivers.'}"
                )
        
        # BUSINESS INSIGHT 2: Profitability analysis
        if revenue_cols and cost_cols:
            rev_col, cost_col = revenue_cols[0], cost_cols[0]
            if isinstance(trends.get(rev_col), dict) and isinstance(trends.get(cost_col), dict):
                rev_change = trends[rev_col].get('change_percentage', 0)
                cost_change = trends[cost_col].get('change_percentage', 0)
                
                if cost_change > rev_change and cost_change > 5:
                    margin_pressure = cost_change - rev_change
                    insights.append(
                        f"⚠️ Profit margin pressure: Costs growing {cost_change:.1f}% while revenue grows {rev_change:.1f}%. "
                        f"Recommend cost optimization review and pricing strategy assessment."
                    )
                elif rev_change > cost_change and rev_change > 10:
                    insights.append(
                        f"✅ Improving profitability: Revenue outpacing costs ({rev_change:.1f}% vs {cost_change:.1f}%). "
                        f"Good operational efficiency - maintain current cost controls."
                    )
        
        # BUSINESS INSIGHT 3: Customer value analysis
        if value_cols and customer_cols:
            val_col = value_cols[0]
            if isinstance(trends.get(val_col), dict):
                val_change = trends[val_col].get('change_percentage', 0)
                
                if val_change < -5:
                    insights.append(
                        f"⚠️ Declining customer value: Average value per customer down {abs(val_change):.1f}%. "
                        f"Investigate product mix changes and consider upselling/cross-selling initiatives to recover value."
                    )
                elif val_change > 10:
                    insights.append(
                        f"✅ Increasing customer value: Up {val_change:.1f}%. "
                        f"Current strategies are working - document and replicate successful tactics."
                    )
        
        # BUSINESS INSIGHT 4: Growth sustainability
        if order_cols and customer_cols:
            if isinstance(trends.get(order_cols[0]), dict) and isinstance(trends.get(customer_cols[0]), dict):
                order_change = trends[order_cols[0]].get('change_percentage', 0)
                cust_change = trends[customer_cols[0]].get('change_percentage', 0)
                
                if order_change > cust_change + 10:
                    insights.append(
                        f"📈 Strong customer engagement: Orders growing faster than customer base ({order_change:.1f}% vs {cust_change:.1f}%). "
                        f"Existing customers are buying more - retention strategies are working."
                    )
        
        # DATA QUALITY INSIGHTS (brief, business-focused)
        missing_pct = df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100
        if missing_pct > 10:
            insights.append(
                f"⚠️ Data completeness issue: {missing_pct:.1f}% missing values may affect analysis accuracy. "
                f"Review data collection processes."
            )
        
        return {'insights': insights} if insights else {'insights': ['Dataset is clean. No significant trends or anomalies detected.']}


def analyze_data(df: pd.DataFrame) -> Dict[str, Any]:
    """Convenience function"""
    analyzer = DataAnalyzer()
    return analyzer.analyze_data(df)
