#!/bin/bash
# Migrate data to Docker named volume
set -e

echo "🔄 Migrating database to named volume..."

# Stop postgres if running
docker-compose down

# Create a temporary container to copy data
docker run --rm \
  -v ./data_backup/postgres:/source:ro \
  -v piper_postgres_data_v1:/target \
  postgres:15 \
  bash -c "cp -Rp /source/* /target/ && chown -R postgres:postgres /target"

echo "✅ Data migrated to named volume!"

# Start postgres again
docker-compose up -d postgres

# Wait for it to be ready
sleep 5

# Verify
docker-compose exec postgres psql -U piper -d piper_morgan -c "\dt" | head -10
