"""Unit tests for SchemaValidator - Issue #484 (ARCH-SCHEMA-VALID)

Tests the schema validation logic that catches model/schema drift at startup.
"""

import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.infrastructure.schema_validator import (
    ColumnMismatch,
    SchemaValidator,
    ValidationResult,
    is_validation_disabled,
)


class TestValidationResult:
    """Tests for ValidationResult dataclass"""

    def test_default_is_valid(self):
        """New ValidationResult should be valid by default"""
        result = ValidationResult()
        assert result.is_valid is True
        assert len(result.mismatches) == 0
        assert result.error is None

    def test_add_mismatch_marks_invalid(self):
        """Adding a mismatch should mark result as invalid"""
        result = ValidationResult()
        mismatch = ColumnMismatch(
            table="test_table",
            column="test_column",
            model_type="UUID",
            schema_type="varchar",
            reason="Type mismatch",
        )
        result.add_mismatch(mismatch)

        assert result.is_valid is False
        assert len(result.mismatches) == 1
        assert result.mismatches[0] == mismatch


class TestColumnMismatch:
    """Tests for ColumnMismatch dataclass"""

    def test_creates_with_all_fields(self):
        """ColumnMismatch should store all diagnostic info"""
        mismatch = ColumnMismatch(
            table="users",
            column="id",
            model_type="UUID",
            schema_type="character varying",
            reason="Type mismatch: model uses UUID, database uses varchar",
        )

        assert mismatch.table == "users"
        assert mismatch.column == "id"
        assert mismatch.model_type == "UUID"
        assert mismatch.schema_type == "character varying"
        assert "Type mismatch" in mismatch.reason


class TestSchemaValidatorTypeMapping:
    """Tests for type compatibility checking"""

    def test_uuid_compatible_with_uuid(self):
        """UUID model type should be compatible with uuid schema type"""
        validator = SchemaValidator()
        assert validator._types_compatible("UUID", "uuid") is True

    def test_string_compatible_with_varchar(self):
        """String model type should be compatible with varchar schema type"""
        validator = SchemaValidator()
        assert validator._types_compatible("String", "varchar") is True
        assert validator._types_compatible("String", "character varying") is True

    def test_uuid_not_compatible_with_varchar(self):
        """UUID model type should NOT be compatible with varchar schema type"""
        validator = SchemaValidator()
        assert validator._types_compatible("UUID", "varchar") is False
        assert validator._types_compatible("UUID", "character varying") is False

    def test_jsonb_compatible_with_jsonb(self):
        """JSONB model type should be compatible with jsonb schema type"""
        validator = SchemaValidator()
        assert validator._types_compatible("JSONB", "jsonb") is True

    def test_integer_compatible_with_int4(self):
        """Integer model type should be compatible with int4 schema type"""
        validator = SchemaValidator()
        assert validator._types_compatible("Integer", "integer") is True
        assert validator._types_compatible("Integer", "int4") is True

    def test_boolean_compatible_with_bool(self):
        """Boolean model type should be compatible with bool schema type"""
        validator = SchemaValidator()
        assert validator._types_compatible("Boolean", "boolean") is True
        assert validator._types_compatible("Boolean", "bool") is True


class TestSchemaValidatorReport:
    """Tests for report generation"""

    def test_valid_report_shows_success(self):
        """Valid result should show success message"""
        validator = SchemaValidator()
        validator.result.tables_checked = 10
        validator.result.columns_checked = 50

        report = validator.get_report()

        assert "Tables checked: 10" in report
        assert "Columns checked: 50" in report
        assert "Mismatches found: 0" in report
        assert "All models match database schema" in report

    def test_invalid_report_shows_mismatches(self):
        """Invalid result should list all mismatches"""
        validator = SchemaValidator()
        validator.result.add_mismatch(
            ColumnMismatch(
                table="todo_items",
                column="owner_id",
                model_type="UUID",
                schema_type="varchar",
                reason="Type mismatch",
            )
        )

        report = validator.get_report()

        assert "Schema drift detected" in report
        assert "todo_items.owner_id" in report
        assert "Model: UUID" in report
        assert "Database: varchar" in report

    def test_error_report_shows_error(self):
        """Report with error should display error message"""
        validator = SchemaValidator()
        validator.result.error = "Connection failed"

        report = validator.get_report()

        assert "ERROR: Connection failed" in report


class TestIsValidationDisabled:
    """Tests for is_validation_disabled function"""

    def test_disabled_when_env_set_to_1(self):
        """Should be disabled when PIPER_SKIP_SCHEMA_VALIDATION=1"""
        with patch.dict(os.environ, {"PIPER_SKIP_SCHEMA_VALIDATION": "1"}):
            assert is_validation_disabled() is True

    def test_enabled_when_env_not_set(self):
        """Should be enabled when env var not set"""
        env_backup = os.environ.get("PIPER_SKIP_SCHEMA_VALIDATION")
        try:
            if "PIPER_SKIP_SCHEMA_VALIDATION" in os.environ:
                del os.environ["PIPER_SKIP_SCHEMA_VALIDATION"]
            assert is_validation_disabled() is False
        finally:
            if env_backup is not None:
                os.environ["PIPER_SKIP_SCHEMA_VALIDATION"] = env_backup

    def test_enabled_when_env_set_to_0(self):
        """Should be enabled when PIPER_SKIP_SCHEMA_VALIDATION=0"""
        with patch.dict(os.environ, {"PIPER_SKIP_SCHEMA_VALIDATION": "0"}):
            assert is_validation_disabled() is False


class TestSchemaValidatorGetModelTypeName:
    """Tests for _get_model_type_name method"""

    def test_recognizes_uuid_type(self):
        """Should recognize PostgreSQL UUID type"""
        from sqlalchemy.dialects.postgresql import UUID

        validator = SchemaValidator()

        col_type = UUID(as_uuid=False)
        assert validator._get_model_type_name(col_type) == "UUID"

    def test_recognizes_jsonb_type(self):
        """Should recognize PostgreSQL JSONB type"""
        from sqlalchemy.dialects.postgresql import JSONB

        validator = SchemaValidator()

        col_type = JSONB()
        assert validator._get_model_type_name(col_type) == "JSONB"

    def test_recognizes_string_type(self):
        """Should recognize String type"""
        from sqlalchemy import String

        validator = SchemaValidator()

        col_type = String(50)
        assert validator._get_model_type_name(col_type) == "String"


class TestSchemaValidatorValidation:
    """Integration-style tests for validation logic"""

    @pytest.mark.asyncio
    async def test_validation_handles_missing_table_gracefully(self):
        """Should handle missing tables without crashing"""
        # Create mock session that returns no rows (table doesn't exist)
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []

        mock_session = AsyncMock()
        mock_session.execute.return_value = mock_result

        validator = SchemaValidator(session=mock_session)

        # Create a mock base with metadata
        mock_base = MagicMock()
        mock_table = MagicMock()
        mock_table.columns = []
        mock_base.metadata.tables = {"missing_table": mock_table}

        # This should not raise, just note the missing table
        result = await validator._do_validation(mock_base)

        # Should complete without error
        assert result.tables_checked == 1

    @pytest.mark.asyncio
    async def test_validation_detects_type_mismatch(self):
        """Should detect when model type doesn't match schema type"""
        from sqlalchemy.dialects.postgresql import UUID

        # Mock session returns varchar for a column that model says is UUID
        mock_result = MagicMock()
        mock_result.fetchall.return_value = [
            MagicMock(
                column_name="owner_id",
                data_type="character varying",
                udt_name="varchar",
                is_nullable="NO",
                column_default=None,
            )
        ]

        mock_session = AsyncMock()
        mock_session.execute.return_value = mock_result

        validator = SchemaValidator(session=mock_session)

        # Create mock column that uses UUID
        mock_column = MagicMock()
        mock_column.name = "owner_id"
        mock_column.type = UUID(as_uuid=False)

        # Create mock base with the UUID column
        mock_base = MagicMock()
        mock_table = MagicMock()
        mock_table.columns = [mock_column]
        mock_base.metadata.tables = {"test_table": mock_table}

        result = await validator._do_validation(mock_base)

        # Should detect the mismatch
        assert result.is_valid is False
        assert len(result.mismatches) == 1
        assert result.mismatches[0].table == "test_table"
        assert result.mismatches[0].column == "owner_id"
        assert result.mismatches[0].model_type == "UUID"
        assert result.mismatches[0].schema_type == "varchar"
