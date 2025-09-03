# Create preservation branch from current position
git checkout -b preserve-docs-20250622

# Commit all the documentation
git add docs/
git commit -m "Preserve comprehensive documentation updates from PM-011 work"

# Add valuable code files
git add tests/test_intent_classification.py
git add services/api/serializers.py
git add services/intent_service/exceptions.py
git add scripts/migrate_add_created_at_to_tasks.py
git commit -m "Preserve architectural improvements: serializers, exceptions, migration script, tests"

# Push to save
git push origin preserve-docs-20250622
