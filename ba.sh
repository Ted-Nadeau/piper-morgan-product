# xian's script shell - please do not move. Oct 4 2025.
# 1. Verify file structure (routers + plugins)
cd ~/Development/piper-morgan
ls -la services/integrations/*/[!test]*.py | wc -l

# 2. Check tests still passing
PYTHONPATH=. python3 -m pytest tests/plugins/ -v | tail -5

# 3. Verify plugin file sizes (should be ~96 lines each)
wc -l services/integrations/*/*_plugin.py

# 4. Check what documentation currently exists
ls -la docs/plugin*.md 2>/dev/null || echo "No plugin docs found"
ls -la services/plugins/README.md

# 5. Check for existing developer guide references
grep -r "developer guide" docs/ 2>/dev/null || echo "No developer guide references"
