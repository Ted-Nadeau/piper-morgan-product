#!/bin/bash
# GREAT-3C Quick Investigation Script
# Determines if plugins are wrappers or substantial implementations

echo "=== GREAT-3C Investigation ==="
echo

echo "1. Current plugin files:"
ls -la services/integrations/*/|grep _plugin.py
echo

echo "2. Plugin class structure (first 30 lines of each):"
echo "--- GitHub Plugin ---"
head -30 services/integrations/github/github_plugin.py
echo
echo "--- Slack Plugin ---"
head -30 services/integrations/slack/slack_plugin.py
echo

echo "3. Plugin implementation check (looking for business logic):"
echo "GitHub plugin line count:"
wc -l services/integrations/github/github_plugin.py
echo "Does it just call router?"
grep -c "self.router" services/integrations/github/github_plugin.py
echo

echo "4. Router dependencies:"
echo "Do plugins import routers?"
grep -l "import.*router" services/integrations/*/_plugin.py
echo

echo "5. What methods do plugins implement?"
grep "def " services/integrations/github/github_plugin.py | head -10
echo

echo "6. Are these thin wrappers or substantial?"
echo "Checking for actual implementation vs delegation:"
echo "GitHub plugin methods with >5 lines:"
awk '/def /{p=1} p{print} /^[[:space:]]*$/{if(p) exit}' services/integrations/github/github_plugin.py | wc -l
