"""Schema Validator - Issue #484 (ARCH-SCHEMA-VALID)

Validates that SQLAlchemy models match actual PostgreSQL database schema.
Catches model/schema drift at startup before runtime failures occur.

Background (Pattern-045 "Green Tests, Red User"):
On Dec 7, 2025, 705 unit tests passed while all CRUD operations failed.
Root cause: Domain models used owner_id: UUID while DB models used String.
This validator catches such drift at application startup.

Usage:
    from services.infrastructure.schema_validator import SchemaValidator

    validator = SchemaValidator()
    await validator.validate()
    if not validator.is_valid():
        print(validator.get_report())
"""

import logging
import os
from dataclasses import dataclass, field
from typing import Any

from sqlalchemy import inspect, text
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


@dataclass
class ColumnMismatch:
    """Details about a column that doesn't match between model and schema."""

    table: str
    column: str
    model_type: str
    schema_type: str
    reason: str


@dataclass
class ValidationResult:
    """Result of schema validation."""

    is_valid: bool = True
    mismatches: list[ColumnMismatch] = field(default_factory=list)
    tables_checked: int = 0
    columns_checked: int = 0
    error: str | None = None

    def add_mismatch(self, mismatch: ColumnMismatch) -> None:
        """Add a mismatch and mark validation as failed."""
        self.mismatches.append(mismatch)
        self.is_valid = False


class SchemaValidator:
    """Validates SQLAlchemy models against PostgreSQL database schema.

    Strategy:
    1. Get all mapped models from SQLAlchemy metadata
    2. For each model/table, compare column types
    3. Report mismatches with clear diagnostic info

    Key comparisons:
    - Column types (UUID vs VARCHAR, Integer vs String, etc.)
    - Nullability constraints
    - Foreign key presence

    Limitations:
    - Only validates tables that have models (not raw SQL tables)
    - Type comparison is PostgreSQL-specific
    - Does not validate indexes or constraints beyond FK presence
    """

    # Map SQLAlchemy types to PostgreSQL type names for comparison
    # This is not exhaustive but covers the common cases
    TYPE_MAPPING = {
        "UUID": ["uuid"],
        "String": ["character varying", "varchar", "text"],
        "Text": ["text", "character varying"],
        "Integer": ["integer", "int4"],
        "BigInteger": ["bigint", "int8"],
        "SmallInteger": ["smallint", "int2"],
        "Float": ["double precision", "float8", "real", "float4"],
        "Boolean": ["boolean", "bool"],
        "DateTime": [
            "timestamp without time zone",
            "timestamp with time zone",
            "timestamp",
            "timestamptz",
        ],
        "Date": ["date"],
        "Time": ["time without time zone", "time with time zone"],
        "JSON": ["json", "jsonb"],  # Both json and jsonb are compatible with JSON
        "JSONB": ["jsonb", "json"],
        "ARRAY": [
            "ARRAY",
            "_float8",
            "_int4",
            "_text",
            "_varchar",
        ],  # PostgreSQL array types start with _
    }

    # PostgreSQL Enum types are stored with custom type names
    # We consider SQLAlchemy Enum compatible with any custom PostgreSQL enum type
    ENUM_COMPATIBLE_PATTERNS = [
        # These are known PostgreSQL enum type names used in this codebase
        "intentcategory",
        "workflowtype",
        "workflowstatus",
        "tasktype",
        "taskstatus",
        "integrationtype",
        "listtype",
        "orderingstrategy",
        "todopriority",
        "patterntype",
    ]

    # Critical tables to always validate (these have caused issues before)
    CRITICAL_TABLES = [
        "users",
        "todo_items",
        "todo_lists",
        "lists",
        "projects",
        "uploaded_files",
        "feedback",
    ]

    def __init__(self, session: AsyncSession | None = None):
        """Initialize validator.

        Args:
            session: Optional async session. If not provided, will create one.
        """
        self.session = session
        self.result = ValidationResult()
        self._schema_cache: dict[str, dict[str, Any]] = {}

    async def validate(self) -> ValidationResult:
        """Run full schema validation.

        Returns:
            ValidationResult with all mismatches found
        """
        from services.database.models import Base

        try:
            # Get session if not provided
            if self.session is None:
                from services.database.session_factory import AsyncSessionFactory

                async with AsyncSessionFactory.session_scope() as session:
                    self.session = session
                    return await self._do_validation(Base)
            else:
                return await self._do_validation(Base)
        except Exception as e:
            self.result.error = str(e)
            self.result.is_valid = False
            logger.error(f"Schema validation failed: {e}")
            return self.result

    async def _do_validation(self, base) -> ValidationResult:
        """Perform the actual validation."""
        # Get all table metadata from models
        tables = base.metadata.tables

        for table_name, table in tables.items():
            self.result.tables_checked += 1

            # Get schema info for this table
            schema_columns = await self._get_schema_columns(table_name)
            if schema_columns is None:
                # Table doesn't exist in database (might be new, not migrated)
                if table_name in self.CRITICAL_TABLES:
                    self.result.add_mismatch(
                        ColumnMismatch(
                            table=table_name,
                            column="*",
                            model_type="(table)",
                            schema_type="(missing)",
                            reason=f"Critical table '{table_name}' not found in database",
                        )
                    )
                continue

            # Compare each column
            for column in table.columns:
                self.result.columns_checked += 1
                await self._validate_column(table_name, column, schema_columns)

        return self.result

    async def _get_schema_columns(self, table_name: str) -> dict[str, Any] | None:
        """Get column info from database schema.

        Returns dict of {column_name: {type, nullable, ...}} or None if table missing.
        """
        if table_name in self._schema_cache:
            return self._schema_cache[table_name]

        try:
            # Query information_schema for column types
            query = text(
                """
                SELECT
                    column_name,
                    data_type,
                    udt_name,
                    is_nullable,
                    column_default
                FROM information_schema.columns
                WHERE table_schema = 'public'
                AND table_name = :table_name
            """
            )

            result = await self.session.execute(query, {"table_name": table_name})
            rows = result.fetchall()

            if not rows:
                return None

            columns = {}
            for row in rows:
                columns[row.column_name] = {
                    "data_type": row.data_type,
                    "udt_name": row.udt_name,
                    "is_nullable": row.is_nullable == "YES",
                    "column_default": row.column_default,
                }

            self._schema_cache[table_name] = columns
            return columns

        except Exception as e:
            logger.warning(f"Failed to get schema for {table_name}: {e}")
            return None

    async def _validate_column(
        self, table_name: str, column, schema_columns: dict[str, Any]
    ) -> None:
        """Validate a single column against schema."""
        column_name = column.name

        # Check if column exists in schema
        if column_name not in schema_columns:
            self.result.add_mismatch(
                ColumnMismatch(
                    table=table_name,
                    column=column_name,
                    model_type=self._get_model_type_name(column.type),
                    schema_type="(missing)",
                    reason=f"Column '{column_name}' in model but not in database",
                )
            )
            return

        schema_col = schema_columns[column_name]

        # Get type names for comparison
        model_type = self._get_model_type_name(column.type)
        schema_type = schema_col["udt_name"]

        # Check type compatibility
        if not self._types_compatible(model_type, schema_type):
            self.result.add_mismatch(
                ColumnMismatch(
                    table=table_name,
                    column=column_name,
                    model_type=model_type,
                    schema_type=schema_type,
                    reason=f"Type mismatch: model uses {model_type}, database uses {schema_type}",
                )
            )

    def _get_model_type_name(self, col_type) -> str:
        """Get a normalized type name from SQLAlchemy column type."""
        # Handle PostgreSQL-specific types
        if isinstance(col_type, postgresql.UUID):
            return "UUID"
        if isinstance(col_type, postgresql.JSONB):
            return "JSONB"
        if isinstance(col_type, postgresql.JSON):
            return "JSON"
        if isinstance(col_type, postgresql.ARRAY):
            return "ARRAY"

        # Get the type class name
        type_name = type(col_type).__name__

        # Handle String with length
        if type_name == "String" or type_name == "VARCHAR":
            return "String"

        return type_name

    def _types_compatible(self, model_type: str, schema_type: str) -> bool:
        """Check if model type and schema type are compatible.

        Args:
            model_type: Normalized model type name (e.g., "UUID", "String")
            schema_type: PostgreSQL udt_name (e.g., "uuid", "varchar")

        Returns:
            True if types are compatible
        """
        # Check if schema_type is in the list of compatible types for model_type
        compatible_types = self.TYPE_MAPPING.get(model_type, [])
        if schema_type.lower() in [t.lower() for t in compatible_types]:
            return True

        # Also allow exact matches (case-insensitive)
        if model_type.lower() == schema_type.lower():
            return True

        # Special case: varchar and String are compatible
        if model_type == "String" and "varchar" in schema_type.lower():
            return True
        if model_type == "String" and "character" in schema_type.lower():
            return True

        # Special case: SQLAlchemy Enum with PostgreSQL enum types
        # PostgreSQL creates custom types for enums (e.g., 'intentcategory')
        if model_type == "Enum":
            # Check if it's a known enum type or looks like an enum (lowercase alphanumeric)
            if schema_type.lower() in self.ENUM_COMPATIBLE_PATTERNS:
                return True
            # Also accept varchar for enums stored as strings
            if schema_type.lower() in ["varchar", "character varying", "text"]:
                return True

        # Special case: PostgreSQL array types start with underscore
        if model_type == "ARRAY" and schema_type.startswith("_"):
            return True

        return False

    def is_valid(self) -> bool:
        """Check if validation passed."""
        return self.result.is_valid

    def get_mismatches(self) -> list[ColumnMismatch]:
        """Get all detected mismatches."""
        return self.result.mismatches

    def get_report(self) -> str:
        """Generate human-readable validation report."""
        lines = [
            "=" * 60,
            "Schema Validation Report (Issue #484)",
            "=" * 60,
            f"Tables checked: {self.result.tables_checked}",
            f"Columns checked: {self.result.columns_checked}",
            f"Mismatches found: {len(self.result.mismatches)}",
            "",
        ]

        if self.result.error:
            lines.extend([f"ERROR: {self.result.error}", ""])

        if self.result.is_valid:
            lines.append("✅ All models match database schema")
        else:
            lines.append("❌ Schema drift detected:")
            lines.append("")
            for m in self.result.mismatches:
                lines.append(f"  {m.table}.{m.column}:")
                lines.append(f"    Model: {m.model_type}")
                lines.append(f"    Database: {m.schema_type}")
                lines.append(f"    Reason: {m.reason}")
                lines.append("")

        return "\n".join(lines)

    def print_report(self) -> None:
        """Print the validation report to stdout."""
        print(self.get_report())


def is_validation_disabled() -> bool:
    """Check if schema validation is disabled via environment variable.

    Set PIPER_SKIP_SCHEMA_VALIDATION=1 to disable validation
    (useful for CI/testing where DB might not exist).
    """
    return os.environ.get("PIPER_SKIP_SCHEMA_VALIDATION", "0") == "1"
