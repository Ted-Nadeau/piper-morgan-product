import pandas as pd
from datetime import datetime
from services.analysis.base_analyzer import BaseAnalyzer
from services.domain.models import AnalysisResult, AnalysisType

class CSVAnalyzer(BaseAnalyzer):
    async def analyze(self, file_path):
        try:
            df = pd.read_csv(file_path)
            row_count = len(df)
            columns = list(df.columns)

            # Statistical summary for numeric columns
            column_stats = {}
            numeric_cols = df.select_dtypes(include=['number']).columns
            for col in numeric_cols:
                col_data = df[col]
                column_stats[col] = {
                    'mean': col_data.mean(),
                    'median': col_data.median(),
                    'min': col_data.min(),
                    'max': col_data.max(),
                    'std': col_data.std()
                }

            # Missing data detection (refactored structure)
            by_column = {}
            total_missing = 0
            for col in columns:
                missing_count = df[col].isnull().sum()
                percent = (missing_count / row_count * 100) if row_count > 0 else 0.0
                by_column[col] = {
                    'count': int(missing_count),
                    'percent': percent
                }
                total_missing += int(missing_count)
            total_cells = row_count * len(columns) if row_count > 0 else 0
            percent_missing = (total_missing / total_cells * 100) if total_cells > 0 else 0.0
            missing_data = {
                'summary': {
                    'total_missing': total_missing,
                    'percent_missing': percent_missing
                },
                'by_column': by_column
            }

            metadata = {
                'row_count': row_count,
                'columns': columns,
                'column_stats': column_stats,
                'missing_data': missing_data
            }
            return AnalysisResult(
                file_id=file_path,
                analysis_type=AnalysisType.DATA,
                summary=f"CSV file with {row_count} rows and {len(columns)} columns.",
                key_findings=[],
                recommendations=[],
                generated_at=datetime.now(),
                metadata=metadata
            )
        except pd.errors.EmptyDataError:
            metadata = {
                'row_count': 0,
                'columns': [],
                'column_stats': {},
                'missing_data': {}
            }
            return AnalysisResult(
                file_id=file_path,
                analysis_type=AnalysisType.DATA,
                summary="Empty CSV file (no data to parse)",
                key_findings=["File contains no parseable data"],
                recommendations=["Ensure file contains valid CSV data"],
                generated_at=datetime.now(),
                metadata=metadata
            )
        except pd.errors.ParserError:
            metadata = {
                'row_count': 0,
                'columns': [],
                'column_stats': {},
                'missing_data': {},
                'error': 'malformed'
            }
            return AnalysisResult(
                file_id=file_path,
                analysis_type=AnalysisType.DATA,
                summary="Malformed CSV file (parse error)",
                key_findings=["File could not be parsed due to malformed structure"],
                recommendations=["Check CSV formatting and consistency"],
                generated_at=datetime.now(),
                metadata=metadata
            ) 