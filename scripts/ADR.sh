#!/bin/bash
# bulk_migrate_adrs.sh

DATABASE_ID="25e11704d8bf80deaac2f806390fe7da"
ADR_DIR="docs/architecture/adr"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

echo "Starting ADR migration to Notion database..."
echo "Database ID: $DATABASE_ID"
echo "Python version: $(python3 --version)"
echo "---"

success_count=0
fail_count=0

for adr in $ADR_DIR/adr-*.md; do
  # Skip the index file
  if [[ "$adr" == *"adr-index.md" ]]; then
    continue
  fi

  filename=$(basename "$adr")
  echo "Publishing: $filename"

  # Use the correct Python command with venv activation
  if source venv/bin/activate && python3 cli/commands/publish.py publish "$adr" --to notion --database "$DATABASE_ID"; then
    ((success_count++))
    echo "  ✓ Success"
  else
    ((fail_count++))
    echo "  ✗ Failed"
  fi

  # Rate limit protection
  sleep 2
done

echo "---"
echo "Migration Complete!"
echo "  Successful: $success_count"
echo "  Failed: $fail_count"
