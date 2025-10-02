# Check file sizes
wc -l main.py web/app.py

# Verify ConfigValidator exists
find . -name "*config*valid*" -type f

# Check router architecture
ls -la services/integration_routers/

# See what's in the monoliths
head -30 main.py
head -30 web/app.py
