import pandas as pd
from services.analysis.base_analyzer import BaseAnalyzer
from services.domain.models import AnalysisResult, AnalysisType
from datetime import datetime

class CSVAnalyzer(BaseAnalyzer):
    def analyze(self, file_path):
        try:
            df = pd.read_csv(file_path)
            row_count = len(df)
            columns = list(df.columns)
            
            # Calculate statistics for numeric columns
            column_stats = {}
            numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
            
            for col in numeric_columns:
                column_stats[col] = {
                    'mean': round(df[col].mean(), 2),
                    'median': round(df[col].median(), 2),
                    'std': round(df[col].std(), 2),
                    'min': round(df[col].min(), 2),
                    'max': round(df[col].max(), 2)
                }
            
            # Calculate missing data
            missing_data = {}
            
            for col in columns:
                missing_count = df[col].isnull().sum()
                missing_percent = round((missing_count / row_count) * 100, 2) if row_count > 0 else 0
                
                missing_data[col] = {
                    'count': int(missing_count),
                    'percent': missing_percent
                }
            
            return AnalysisResult(
                file_id=file_path,
                analysis_type=AnalysisType.DATA,
                summary=f"CSV file with {row_count} rows and {len(columns)} columns.",
                key_findings=[],
                metadata={
                    'row_count': row_count,
                    'columns': columns,
                    'column_stats': column_stats,
                    'missing_data': missing_data
                },
                recommendations=[],
                generated_at=datetime.now(),
                filename=file_path
            )
            
        except pd.errors.ParserError as e:
            return AnalysisResult(
                file_id=file_path,
                analysis_type=AnalysisType.DATA,
                summary="Unable to parse CSV file due to malformed data structure.",
                key_findings=[],
                metadata={
                    'error': 'malformed',
                    'error_details': str(e)
                },
                recommendations=[],
                generated_at=datetime.now(),
                filename=file_path
            ) 