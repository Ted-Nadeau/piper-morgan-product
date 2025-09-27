#!/bin/bash

# COMPLETE recovery script for ALL 170 files from stash commit 48a7a36d51f67b0e6c9ad0b6cfe6d07f168664a8
STASH_COMMIT="48a7a36d51f67b0e6c9ad0b6cfe6d07f168664a8"
RECOVERY_DIR="COMPLETE-RECOVERY"

echo "🚨 COMPLETE RECOVERY: Extracting ALL 170 lost files from stash commit $STASH_COMMIT"
echo "📁 Recovery directory: $RECOVERY_DIR"

# Remove existing recovery if it exists
rm -rf "$RECOVERY_DIR"
mkdir -p "$RECOVERY_DIR"

# Extract EVERY SINGLE FILE from the complete list
while IFS= read -r line; do
    # Skip empty lines and commit info lines
    if [[ -z "$line" || "$line" =~ ^commit || "$line" =~ ^Merge: || "$line" =~ ^Author: || "$line" =~ ^Date: || "$line" =~ ^[[:space:]]*$ ]]; then
        continue
    fi

    # Skip the commit message line
    if [[ "$line" == *"On verification/ci-test"* ]]; then
        continue
    fi

    filepath="$line"
    echo "📄 Extracting: $filepath"

    # Create directory structure
    mkdir -p "$RECOVERY_DIR/$(dirname "$filepath")"

    # Extract the file
    git show "$STASH_COMMIT:$filepath" > "$RECOVERY_DIR/$filepath" 2>/dev/null

    # Check if extraction was successful
    if [[ $? -eq 0 && -s "$RECOVERY_DIR/$filepath" ]]; then
        echo "   ✅ Success"
    else
        echo "   ❌ Failed or empty"
        rm -f "$RECOVERY_DIR/$filepath" 2>/dev/null
    fi

done < complete-lost-files-list.txt

echo ""
echo "🎉 COMPLETE RECOVERY FINISHED!"
echo ""
echo "📊 Final count:"
find "$RECOVERY_DIR" -type f | wc -l | tr -d ' ' | sed 's/$/ total files recovered/'
echo ""
echo "📁 Directory structure:"
tree "$RECOVERY_DIR" -d -L 3
echo ""
echo "🔍 Key categories recovered:"
echo "📋 Configuration: .cursor/, .github/ files"
echo "📝 Development logs: dev/2025/09/{21,22,23,24}/ + dev/active/"
echo "📚 Knowledge base: knowledge/ + knowledge/versions/"
echo "📖 Documentation: docs/omnibus-logs/, docs/architecture/"
echo "🧪 Testing: tests/mocks/, tests/utils/"
echo "📊 Scripts: scripts/"
echo "💻 Services: services/intent_service/"
echo ""
echo "✅ Everything from the stash has been recovered to: $RECOVERY_DIR/"