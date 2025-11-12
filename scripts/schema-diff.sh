#!/bin/bash
# Schema Diff Script
# Compare current database schema with models

echo "=========================================="
echo "Schema Comparison Script"
echo "=========================================="

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo ""
echo "Comparing database schema with SQLAlchemy models..."

# Generate current schema
echo "1. Dumping current database schema..."
docker exec piper-postgres pg_dump -U piper -d piper_morgan --schema-only > /tmp/current_schema.sql 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Current schema dumped"
else
    echo -e "${RED}✗${NC} Failed to dump current schema"
    exit 1
fi

# Check if alembic can detect any changes
echo ""
echo "2. Checking for model/schema differences..."
AUTOGEN_OUTPUT=$(alembic revision --autogenerate -m "temp_schema_check" 2>&1)

# Check if any operations were detected
if echo "$AUTOGEN_OUTPUT" | grep -q "No changes in schema detected"; then
    echo -e "${GREEN}✓${NC} Schema matches models perfectly"
    echo ""
    echo "Result: No migration needed - database and models are in sync"

    # Clean up the temp revision file
    TEMP_REV=$(ls -t alembic/versions/*.py | head -1)
    if [ -f "$TEMP_REV" ] && grep -q "temp_schema_check" "$TEMP_REV"; then
        rm "$TEMP_REV"
        echo "   (Cleaned up temporary revision file)"
    fi

elif echo "$AUTOGEN_OUTPUT" | grep -q "Generating"; then
    echo -e "${YELLOW}⚠${NC} Differences detected between schema and models"
    echo ""
    echo "A temporary migration file was created showing the differences."
    echo "Review the latest file in alembic/versions/ to see what changed."
    echo ""
    echo -e "${YELLOW}Action needed${NC}: Either apply the migration or update your models"

    # Show the temp revision file location
    TEMP_REV=$(ls -t alembic/versions/*.py | head -1)
    echo "   Temporary revision: $TEMP_REV"
    echo ""
    echo "To clean up: rm $TEMP_REV"

else
    echo -e "${RED}✗${NC} Failed to generate schema comparison"
    echo "$AUTOGEN_OUTPUT"
    exit 1
fi

# Cleanup
rm -f /tmp/current_schema.sql

echo ""
echo "=========================================="
echo "Schema comparison complete"
echo "=========================================="
