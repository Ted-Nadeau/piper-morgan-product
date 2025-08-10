# Check what test files we have
find tests -name "*analyz*" -type f
find services/analysis/tests -name "*.py" -type f

# If test files exist, we can run them to verify our recreated code
pytest services/analysis/tests/ -v

# Or if they're in the main tests directory
pytest tests/ -k "analyz" -v
