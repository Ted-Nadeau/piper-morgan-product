#!/bin/bash
# Publish "Wiring vs. Wizardry" to pipermorgan.ai
# Run from piper-morgan-product repo root on your local machine
# Generated: 2026-03-29

set -e

SLUG="wiring-vs-wizardry"
HASH_ID="a2ba24488d1c"
TITLE="Wiring vs. Wizardry"
WORK_DATE="2026-03-13"
PUB_DATE="2026-03-30"
CATEGORY="insight"
IMAGE_SLUG="wiring-vs-wizardry"
CHAT_DATE="3/13/2026"
WEBSITE_REPO="../piper-morgan-website"

echo "=== Step 1: Verify website repo ==="
if [ ! -d "$WEBSITE_REPO" ]; then
    echo "ERROR: Website repo not found at $WEBSITE_REPO"
    exit 1
fi
cd "$WEBSITE_REPO"
git checkout main
git pull origin main
echo "✓ Website repo ready"

echo ""
echo "=== Step 2: Convert and copy image ==="
IMAGE_SOURCE="dev/active/ai-wiring-compressed.png"
if [ -f "$IMAGE_SOURCE" ]; then
    if command -v cwebp &> /dev/null; then
        cwebp "$IMAGE_SOURCE" -o "public/assets/blog-images/${IMAGE_SLUG}.webp"
        echo "✓ Image converted to webp"
    else
        cp "$IMAGE_SOURCE" "public/assets/blog-images/${IMAGE_SLUG}.png"
        echo "⚠ cwebp not found, using PNG (install with: brew install webp)"
    fi
else
    echo "⚠ Image not found at $IMAGE_SOURCE"
    echo "  Trying alternate locations..."
    for alt in "dev/active/ai-wiring.png" "dev/active/wiring-vs-wizardry.png"; do
        if [ -f "$alt" ]; then
            echo "  Found at $alt"
            if command -v cwebp &> /dev/null; then
                cwebp "$alt" -o "public/assets/blog-images/${IMAGE_SLUG}.webp"
                echo "✓ Image converted to webp"
            else
                cp "$alt" "public/assets/blog-images/${IMAGE_SLUG}.png"
            fi
            break
        fi
    done
fi

echo ""
echo "=== Step 3: Add to blog-metadata.csv ==="
python3 -c "
import csv, os
filepath = 'data/blog-metadata.csv'
with open(filepath, 'rb') as f:
    f.seek(-1, 2)
    if f.read(1) != b'\n':
        with open(filepath, 'a') as fa:
            fa.write('\n')
with open(filepath, 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['${SLUG}', '${HASH_ID}', '${TITLE}', '${CHAT_DATE}', '${IMAGE_SLUG}.webp', '${WORK_DATE}', '${PUB_DATE}', '${CATEGORY}', '', '', ''])
print('✓ Added to blog-metadata.csv')
"

echo ""
echo "=== Step 4: Add blog content ==="
python3 << 'PYEOF'
import json

html_path = 'dev/active/publish-package/wiring-vs-wizardry-content.html'
with open(html_path) as f:
    html = f.read()

content_path = 'src/data/blog-content.json'
with open(content_path) as f:
    content = json.load(f)

content['a2ba24488d1c'] = {'content': html}

with open(content_path, 'w') as f:
    json.dump(content, f, indent=2)

print('✓ Added content to blog-content.json')
PYEOF

echo ""
echo "=== Step 5: Run sync and fetch ==="
node scripts/sync-csv-to-json.js
echo "✓ CSV synced to JSON"
node scripts/fetch-blog-posts.js
echo "✓ Blog posts fetched"

echo ""
echo "=== Step 6: Verify ==="
python3 -c "
import json
posts = json.load(open('src/data/medium-posts.json'))
match = [p for p in posts if 'wiring' in p.get('slug','').lower() or 'wiring' in p.get('title','').lower()]
for p in match:
    print(f\"  Title: {p['title']}\")
    print(f\"  URL: {p.get('url','')}\")
    print(f\"  Slug: {p.get('slug','')}\")
if not match:
    print('  ⚠ Post not found in medium-posts.json — check manually')
"

echo ""
echo "=== Step 7: Commit and push ==="
git add data/blog-metadata.csv src/data/medium-posts.json src/data/blog-content.json public/assets/blog-images/
git commit -m "Add blog post: Wiring vs. Wizardry"
git push origin main
echo "✓ Website repo pushed"

echo ""
echo "=== Done! ==="
echo "Verify at: https://pipermorgan.ai/blog/${SLUG}"
echo ""
echo "After verifying, syndicate to:"
echo "  1. Medium — paste content, set canonical URL to https://pipermorgan.ai/blog/${SLUG}"
echo "  2. LinkedIn — cross-post if desired"
