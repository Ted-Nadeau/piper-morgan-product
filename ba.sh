# 1. Serena operational?
serena --version

# 2. Documentation accessible?
ls -la docs/architecture/
ls -la docs/adrs/

# 3. CI/CD status visible?
gh workflow list

# 4. Test baseline known?
pytest --collect-only
