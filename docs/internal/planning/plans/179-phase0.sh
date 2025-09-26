cd ../../../

# 1. Check orchestration service initialization
grep -n "OrchestrationEngine" services/orchestration/engine.py | head -5
grep -n "__init__" services/orchestration/engine.py

# 2. Check for workflow factory patterns
grep -n "create_workflow_from_intent" services/orchestration/*.py

# 3. Look for query action definitions
grep -r "show_standup\|query_action" services/ --include="*.py"

# 4. Check if orchestration service is running
ps aux | grep -E "orchestration|engine" | grep -v grep

# 5. Find intent to workflow mapping
find services/ -name "*.json" -o -name "*.yaml" | xargs grep -l "intent\|workflow" 2>/dev/null
