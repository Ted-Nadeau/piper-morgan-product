cd /Users/xian/Development/piper-morgan/archive/piper-morgan-0.1.1/

# Find the ChromaDB database location
find . -name "*.sqlite*" -o -name "chroma*" -type d

# Create a backup
mkdir -p backups/$(date +%Y%m%d_%H%M%S)
cp -r ./chroma* backups/$(date +%Y%m%d_%H%M%S)/ 2>/dev/null || echo "No chroma directory found"
cp *.sqlite* backups/$(date +%Y%m%d_%H%M%S)/ 2>/dev/null || echo "No sqlite files found"
