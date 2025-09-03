# Create a new branch from your current position to save docs
git checkout -b preserve-docs-20250622

# Add only documentation files
git add docs/
git commit -m "Preserve comprehensive documentation updates from PM-011 work"

# Also add the test file - it's valuable
git add tests/test_intent_classification.py
git commit -m "Add intent classification tests"

# Save other potentially useful files
git add services/api/serializers.py
git add services/intent_service/exceptions.py
git add scripts/migrate_add_created_at_to_tasks.py
git commit -m "Preserve architectural improvements: serializers, exceptions, migration script"

# Push this branch to save it
git push origin preserve-docs-20250622
