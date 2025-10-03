# Check if pytest is installed in virtual environment
which python
python3 -m pytest --version

# Check for test running scripts
ls -la *.sh | grep test

# Look for how tests were run in GREAT-3A
grep -r "pytest" dev/2025/10/02/*.md | head -5

# Check project structure for test configuration
ls -la pytest.ini pyproject.toml setup.cfg 2>/dev/null

# Try running tests the way they were run yesterday
cd ~/Development/piper-morgan && python3 -m pytest tests/plugins/ -v --tb=line 2>&1 | tail -30
