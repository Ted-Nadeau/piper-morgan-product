# Claude Code Prompt: GREAT-2E Phase 0 - Technical Documentation Verification

## Mission: Documentation Technical Verification & Link Analysis

**Context**: GREAT-2E scope likely reduced due to weekend documentation work. Phase 0 investigation to determine actual remaining work needed for documentation completeness.

**Objective**: Comprehensive technical verification of documentation links, CI integration, pattern implementations, and ADR accuracy to identify real gaps requiring attention.

## Phase 0 Investigation Tasks

### Task 1: Comprehensive Link Validation

Test documentation links systematically, excluding legacy/archive content:

```bash
# Find all markdown files with links
echo "=== COMPREHENSIVE LINK ANALYSIS ==="

echo "📄 Finding documentation files with links..."
find docs/ -name "*.md" -exec grep -l "http\|\.md\|\.html" {} \; | head -20

echo ""
echo "🔗 Analyzing link types in documentation..."

# Count different link types
echo "HTTP links:"
find docs/ -name "*.md" -exec grep -h "http" {} \; | wc -l

echo "Internal markdown links:"
find docs/ -name "*.md" -exec grep -h "\.md" {} \; | wc -l

echo "HTML links:"
find docs/ -name "*.md" -exec grep -h "\.html" {} \; | wc -l

# Sample links for testing
echo ""
echo "📋 Sample links found for testing:"
find docs/ -name "*.md" -exec grep -h "http\|\.md\|\.html" {} \; | head -10

# Check for legacy/archive exclusions
echo ""
echo "🗄️ Checking for legacy/archive documentation..."
find docs/ -name "*legacy*" -o -name "*archive*" -o -name "*old*" | head -10

# Check specific pattern documentation
echo ""
echo "📚 Pattern documentation link analysis..."
ls -la docs/patterns/ 2>/dev/null || echo "No patterns directory found"

if [ -d "docs/patterns" ]; then
    echo "Pattern files with links:"
    find docs/patterns/ -name "*.md" -exec grep -l "http\|\.md" {} \; | head -10
fi
```

### Task 2: CI Workflow Analysis

Verify link checker presence and configuration:

```bash
# Check CI workflows for link checking
echo "=== CI WORKFLOW ANALYSIS ==="

echo "📁 CI workflow files:"
ls -la .github/workflows/

echo ""
echo "🔍 Searching for link checker in workflows..."
grep -r "link" .github/workflows/ || echo "No link-related workflows found"

echo ""
echo "🔍 Searching for specific link checker tools..."
grep -r "linkchecker\|link.*check\|broken.*link" .github/workflows/ || echo "No link checker tools found"

echo ""
echo "📄 Checking individual workflow files..."
for workflow in .github/workflows/*.yml .github/workflows/*.yaml; do
    if [ -f "$workflow" ]; then
        echo "--- $(basename $workflow) ---"
        grep -n "link\|check" "$workflow" | head -5 || echo "No link checking found"
    fi
done

# Check for documentation-related workflows
echo ""
echo "📚 Documentation-specific workflows..."
ls .github/workflows/ | grep -i "doc\|link"
```

### Task 3: Pattern Implementation Verification

Verify pattern catalog accuracy and current status:

```python
# Analyze pattern implementation status
def analyze_pattern_implementation():
    """Analyze pattern catalog vs actual implementation"""
    
    print("=== PATTERN IMPLEMENTATION VERIFICATION ===")
    
    import os
    import glob
    
    # Check patterns directory structure
    patterns_dir = "docs/patterns"
    
    if os.path.exists(patterns_dir):
        print(f"✅ Patterns directory exists: {patterns_dir}")
        
        # List pattern files
        pattern_files = glob.glob(f"{patterns_dir}/*.md")
        print(f"📁 Pattern files found: {len(pattern_files)}")
        
        for pattern_file in pattern_files[:10]:  # Show first 10
            filename = os.path.basename(pattern_file)
            print(f"  - {filename}")
        
        # Check for README or index
        readme_files = glob.glob(f"{patterns_dir}/README*") + glob.glob(f"{patterns_dir}/index*")
        print(f"📖 Pattern index files: {len(readme_files)}")
        
        for readme in readme_files:
            print(f"  - {os.path.basename(readme)}")
            
    else:
        print(f"❌ Patterns directory not found: {patterns_dir}")
        
        # Check alternative locations
        alt_locations = [
            "docs/architecture/patterns",
            "docs/internal/patterns", 
            "patterns",
            "design-patterns"
        ]
        
        for alt_loc in alt_locations:
            if os.path.exists(alt_loc):
                print(f"🔍 Alternative patterns location found: {alt_loc}")
                break
    
    # Check for pattern references in codebase
    print(f"\n🔍 Pattern references in codebase...")
    
    try:
        import subprocess
        result = subprocess.run(
            ["grep", "-r", "Pattern-", "services/", "--include=*.py"], 
            capture_output=True, text=True
        )
        
        if result.stdout:
            pattern_refs = result.stdout.strip().split('\n')
            print(f"Pattern references in code: {len(pattern_refs)}")
            
            # Show unique pattern references
            unique_patterns = set()
            for ref in pattern_refs[:20]:  # First 20 references
                if "Pattern-" in ref:
                    # Extract pattern number/name
                    import re
                    pattern_match = re.search(r'Pattern-\d+', ref)
                    if pattern_match:
                        unique_patterns.add(pattern_match.group())
            
            print(f"Unique patterns referenced: {len(unique_patterns)}")
            for pattern in sorted(unique_patterns):
                print(f"  - {pattern}")
        else:
            print("No pattern references found in codebase")
            
    except Exception as e:
        print(f"Error searching for pattern references: {e}")

analyze_pattern_implementation()
```

### Task 4: ADR Currency Verification

Verify ADRs reflect current system reality:

```python
# Verify ADR currency and accuracy
def verify_adr_currency():
    """Check ADR currency against current implementation"""
    
    print("=== ADR CURRENCY VERIFICATION ===")
    
    import os
    import glob
    from datetime import datetime
    
    # Find ADR directories
    adr_locations = [
        "docs/internal/architecture/current/adrs",
        "docs/architecture/adrs", 
        "docs/adrs",
        "adrs"
    ]
    
    adr_dir = None
    for location in adr_locations:
        if os.path.exists(location):
            adr_dir = location
            print(f"✅ ADRs found in: {adr_dir}")
            break
    
    if not adr_dir:
        print("❌ No ADR directory found")
        return
    
    # List ADR files
    adr_files = glob.glob(f"{adr_dir}/*.md")
    print(f"📄 ADR files found: {len(adr_files)}")
    
    # Analyze ADR file dates and content
    adr_analysis = []
    
    for adr_file in adr_files:
        try:
            filename = os.path.basename(adr_file)
            
            # Get file modification time
            mod_time = os.path.getmtime(adr_file)
            mod_date = datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d")
            
            # Read first few lines for status and context
            with open(adr_file, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')[:20]  # First 20 lines
            
            # Look for status
            status = "Unknown"
            for line in lines:
                if line.startswith("## Status") or line.startswith("**Status"):
                    # Try to get next line
                    line_idx = lines.index(line)
                    if line_idx + 1 < len(lines):
                        status = lines[line_idx + 1].strip()
                    break
            
            adr_analysis.append({
                'file': filename,
                'modified': mod_date,
                'status': status,
                'size': len(content)
            })
            
        except Exception as e:
            print(f"Error analyzing {adr_file}: {e}")
    
    # Show ADR analysis
    print(f"\n📊 ADR Analysis:")
    for adr in sorted(adr_analysis, key=lambda x: x['modified'], reverse=True)[:10]:
        print(f"  {adr['file']}: {adr['status']} (Modified: {adr['modified']}, {adr['size']} chars)")
    
    # Check for specific ADRs mentioned in GREAT-2D
    key_adrs = ["adr-038", "spatial-intelligence", "delegated-mcp"]
    
    print(f"\n🔍 Key ADR verification:")
    for key_adr in key_adrs:
        found_files = [adr for adr in adr_analysis if key_adr.lower() in adr['file'].lower()]
        if found_files:
            for found in found_files:
                print(f"  ✅ {key_adr}: {found['file']} (Modified: {found['modified']})")
        else:
            print(f"  ❌ {key_adr}: Not found")
    
    # Check for outdated references
    print(f"\n⚠️ Potentially outdated ADRs (>30 days old):")
    recent_threshold = datetime.now().timestamp() - (30 * 24 * 60 * 60)  # 30 days ago
    
    outdated_count = 0
    for adr_file in adr_files:
        mod_time = os.path.getmtime(adr_file)
        if mod_time < recent_threshold:
            filename = os.path.basename(adr_file)
            mod_date = datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d")
            print(f"  📅 {filename}: {mod_date}")
            outdated_count += 1
    
    if outdated_count == 0:
        print("  ✅ All ADRs recently updated")
    
    return adr_analysis

adr_analysis = verify_adr_currency()
```

### Task 5: Link Testing Implementation

Implement basic link testing to identify broken links:

```python
# Test documentation links for validity
def test_documentation_links():
    """Test sample documentation links for validity"""
    
    print("=== LINK TESTING IMPLEMENTATION ===")
    
    import os
    import glob
    import re
    import requests
    from urllib.parse import urljoin, urlparse
    
    # Find markdown files
    doc_files = glob.glob("docs/**/*.md", recursive=True)
    print(f"📄 Documentation files to analyze: {len(doc_files)}")
    
    # Extract links
    all_links = []
    internal_links = []
    external_links = []
    
    for doc_file in doc_files[:10]:  # Test first 10 files
        try:
            with open(doc_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find markdown links [text](url)
            markdown_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
            
            for link_text, link_url in markdown_links:
                link_info = {
                    'file': doc_file,
                    'text': link_text,
                    'url': link_url,
                    'type': 'unknown'
                }
                
                if link_url.startswith('http'):
                    link_info['type'] = 'external'
                    external_links.append(link_info)
                elif link_url.endswith('.md') or '/' in link_url:
                    link_info['type'] = 'internal'
                    internal_links.append(link_info)
                
                all_links.append(link_info)
                
        except Exception as e:
            print(f"Error reading {doc_file}: {e}")
    
    print(f"🔗 Total links found: {len(all_links)}")
    print(f"🌐 External links: {len(external_links)}")
    print(f"📄 Internal links: {len(internal_links)}")
    
    # Test sample external links
    print(f"\n🧪 Testing sample external links...")
    
    broken_links = []
    working_links = []
    
    for link in external_links[:5]:  # Test first 5 external links
        try:
            print(f"Testing: {link['url']}")
            
            response = requests.head(link['url'], timeout=10, allow_redirects=True)
            
            if response.status_code < 400:
                working_links.append(link)
                print(f"  ✅ {response.status_code}: {link['url']}")
            else:
                broken_links.append(link)
                print(f"  ❌ {response.status_code}: {link['url']}")
                
        except Exception as e:
            broken_links.append(link)
            print(f"  ❌ Error: {link['url']} - {str(e)[:50]}")
    
    # Test sample internal links
    print(f"\n📄 Testing sample internal links...")
    
    for link in internal_links[:5]:  # Test first 5 internal links
        link_path = link['url']
        
        # Handle relative paths
        if not link_path.startswith('/'):
            # Relative to current file
            current_dir = os.path.dirname(link['file'])
            full_path = os.path.join(current_dir, link_path)
            full_path = os.path.normpath(full_path)
        else:
            full_path = link_path[1:]  # Remove leading /
        
        if os.path.exists(full_path):
            print(f"  ✅ {link['url']} -> {full_path}")
        else:
            print(f"  ❌ {link['url']} -> {full_path} (not found)")
            broken_links.append(link)
    
    # Summary
    print(f"\n📊 Link Testing Summary:")
    print(f"  Total tested: {min(len(external_links), 5) + min(len(internal_links), 5)}")
    print(f"  Working: {len(working_links)}")
    print(f"  Broken: {len(broken_links)}")
    
    if broken_links:
        print(f"\n❌ Broken links found:")
        for broken in broken_links:
            print(f"  {broken['file']}: {broken['url']}")
    else:
        print(f"\n✅ No broken links in sample")
    
    return {
        'total_links': len(all_links),
        'external_links': len(external_links),
        'internal_links': len(internal_links),
        'tested_links': min(len(external_links), 5) + min(len(internal_links), 5),
        'broken_links': broken_links,
        'working_links': working_links
    }

# Skip link testing if requests not available
try:
    import requests
    link_test_results = test_documentation_links()
except ImportError:
    print("=== LINK TESTING IMPLEMENTATION ===")
    print("⚠️ requests module not available - will implement link testing in next phase")
    link_test_results = {'testing_skipped': True}
```

## Success Criteria

Phase 0 complete when:
- [✅] Comprehensive link analysis performed
- [✅] CI workflow analysis complete
- [✅] Pattern implementation verification done
- [✅] ADR currency assessment complete
- [✅] Link testing strategy implemented
- [✅] Actual remaining work identified

---

**Your Mission**: Conduct comprehensive technical verification of documentation infrastructure to determine exact scope of remaining work for GREAT-2E completion.

**Quality Standard**: Thorough analysis enabling accurate scope assessment and efficient implementation planning.
