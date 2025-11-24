# Quick infrastructure verification
ls -la web/api/routes/          # What routes exist?
ls -la services/intent_service/  # Handler structure?
grep -r "class.*Todo" services/  # Todo service exists?
find . -name "*todo*" -type f    # All todo-related files?
