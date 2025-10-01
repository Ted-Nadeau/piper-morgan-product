# Cursor Agent Prompt: GREAT-2E Phase 0 - Documentation Organization Verification

## Mission: Documentation Structure & Organization Analysis

**Context**: GREAT-2E scope likely reduced due to weekend documentation work and continuous GREAT-2 improvements. Phase 0 investigation to determine documentation organization status and remaining gaps.

**Objective**: Comprehensive analysis of documentation structure, organization, accessibility, and completeness to identify areas needing attention for final GREAT-2E completion.

## Phase 0 Investigation Tasks

### Task 1: Documentation Structure Analysis

Map complete documentation ecosystem and organization:

```bash
# Comprehensive documentation structure analysis
echo "=== DOCUMENTATION STRUCTURE ANALYSIS ==="

echo "📁 Top-level documentation structure:"
find docs/ -maxdepth 2 -type d | sort

echo ""
echo "📄 Documentation file distribution:"
echo "Total markdown files:"
find . -name "*.md" | wc -l

echo "Documentation directory files:"
find docs/ -name "*.md" | wc -l

echo "Root documentation files:"
find . -maxdepth 1 -name "*.md" | wc -l

echo ""
echo "📊 Documentation by category:"
echo "Architecture docs:"
find docs/ -path "*architecture*" -name "*.md" | wc -l

echo "Pattern docs:"
find docs/ -path "*pattern*" -name "*.md" | wc -l

echo "Operations docs:"
find docs/ -path "*operation*" -name "*.md" | wc -l

echo "Integration docs:"
find docs/ -path "*integration*" -name "*.md" | wc -l

echo ""
echo "🔍 Key documentation files:"
ls -la docs/NAVIGATION.md docs/README.md README.md 2>/dev/null || echo "Standard navigation files not found"

# Check for documentation indexes
echo ""
echo "📖 Documentation indexes and catalogs:"
find docs/ -name "*index*" -o -name "*catalog*" -o -name "*navigation*" | head -10
```

### Task 2: Link Organization and Categorization

Analyze link organization patterns and identify categories:

```bash
# Link organization analysis
echo "=== LINK ORGANIZATION ANALYSIS ==="

echo "🔗 Link distribution analysis:"

# Find files with external links
echo "Files with external HTTP links:"
find docs/ -name "*.md" -exec grep -l "http://" {} \; | wc -l

echo "Files with external HTTPS links:"
find docs/ -name "*.md" -exec grep -l "https://" {} \; | wc -l

echo "Files with internal markdown links:"
find docs/ -name "*.md" -exec grep -l "\.md)" {} \; | wc -l

echo ""
echo "📋 Link categories in documentation:"

# Analyze link patterns
echo "GitHub links:"
find docs/ -name "*.md" -exec grep -h "github\.com" {} \; | wc -l

echo "Internal relative links:"
find docs/ -name "*.md" -exec grep -h "\]\(\.\/" {} \; | wc -l

echo "Internal absolute links:"
find docs/ -name "*.md" -exec grep -h "\]\(\/" {} \; | wc -l

echo ""
echo "🗂️ Documentation with most links:"
find docs/ -name "*.md" -exec sh -c 'echo "$(grep -c "](.*)" "$1"): $1"' _ {} \; | sort -nr | head -5

# Check for link organization patterns
echo ""
echo "📚 Documentation organization patterns:"
echo "Table of contents files:"
find docs/ -name "*.md" -exec grep -l "Table of Contents\|TOC\|Navigation" {} \; | head -5

echo "Index files:"
find docs/ -name "*index*.md" | head -5

echo "README files in subdirectories:"
find docs/ -mindepth 2 -name "README.md" | head -5
```

### Task 3: Pattern Catalog Completeness Review

Verify pattern catalog organization and completeness:

```python
# Pattern catalog analysis
def analyze_pattern_catalog():
    """Analyze pattern catalog organization and completeness"""
    
    print("=== PATTERN CATALOG COMPLETENESS REVIEW ===")
    
    import os
    import glob
    import re
    
    # Check for pattern directories
    pattern_locations = [
        "docs/patterns",
        "docs/architecture/patterns", 
        "docs/internal/patterns",
        "patterns"
    ]
    
    pattern_dir = None
    for location in pattern_locations:
        if os.path.exists(location):
            pattern_dir = location
            print(f"✅ Pattern directory found: {pattern_dir}")
            break
    
    if not pattern_dir:
        print("❌ No pattern directory found")
        
        # Check for pattern files in other locations
        print("🔍 Searching for pattern files elsewhere...")
        pattern_files = glob.glob("**/*pattern*.md", recursive=True)
        print(f"Pattern files found: {len(pattern_files)}")
        for pf in pattern_files[:5]:
            print(f"  - {pf}")
        return
    
    # Analyze pattern directory structure
    pattern_files = glob.glob(f"{pattern_dir}/*.md")
    print(f"📄 Pattern files: {len(pattern_files)}")
    
    # Check for pattern naming conventions
    numbered_patterns = []
    template_patterns = []
    other_patterns = []
    
    for pattern_file in pattern_files:
        filename = os.path.basename(pattern_file)
        
        # Check for numbered patterns (pattern-001-name.md)
        if re.match(r'pattern-\d+.*\.md', filename):
            numbered_patterns.append(filename)
        elif 'template' in filename.lower():
            template_patterns.append(filename)
        else:
            other_patterns.append(filename)
    
    print(f"📊 Pattern organization:")
    print(f"  Numbered patterns: {len(numbered_patterns)}")
    print(f"  Template patterns: {len(template_patterns)}")
    print(f"  Other patterns: {len(other_patterns)}")
    
    # Show pattern sequence
    if numbered_patterns:
        print(f"\n🔢 Pattern sequence (first 10):")
        for pattern in sorted(numbered_patterns)[:10]:
            print(f"  - {pattern}")
        
        # Check for gaps in sequence
        pattern_numbers = []
        for pattern in numbered_patterns:
            match = re.search(r'pattern-(\d+)', pattern)
            if match:
                pattern_numbers.append(int(match.group(1)))
        
        if pattern_numbers:
            pattern_numbers.sort()
            print(f"\n📈 Pattern sequence analysis:")
            print(f"  Range: {min(pattern_numbers)} to {max(pattern_numbers)}")
            print(f"  Total numbered: {len(pattern_numbers)}")
            
            # Check for gaps
            expected = list(range(min(pattern_numbers), max(pattern_numbers) + 1))
            missing = [n for n in expected if n not in pattern_numbers]
            
            if missing:
                print(f"  ⚠️ Missing pattern numbers: {missing}")
            else:
                print(f"  ✅ No gaps in pattern sequence")
    
    # Check for pattern index/catalog files
    print(f"\n📖 Pattern catalog files:")
    catalog_files = glob.glob(f"{pattern_dir}/README*") + glob.glob(f"{pattern_dir}/*index*") + glob.glob(f"{pattern_dir}/*catalog*")
    
    if catalog_files:
        for catalog in catalog_files:
            filename = os.path.basename(catalog)
            
            with open(catalog, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = len(content.split('\n'))
            
            print(f"  ✅ {filename}: {lines} lines")
            
            # Check if catalog references all patterns
            referenced_patterns = len(re.findall(r'pattern-\d+', content.lower()))
            print(f"    References to numbered patterns: {referenced_patterns}")
            
    else:
        print(f"  ❌ No pattern catalog files found")
    
    # Check pattern content quality
    print(f"\n📝 Pattern content analysis:")
    
    sample_patterns = numbered_patterns[:3] if numbered_patterns else pattern_files[:3]
    
    for pattern_file in sample_patterns:
        full_path = os.path.join(pattern_dir, pattern_file)
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic content checks
            has_title = content.startswith('#')
            has_sections = content.count('##') >= 3
            has_code = '```' in content
            has_links = '](' in content
            
            print(f"  📄 {pattern_file}:")
            print(f"    Lines: {len(content.split('\n'))}")
            print(f"    Has title: {has_title}")
            print(f"    Has sections: {has_sections}")
            print(f"    Has code examples: {has_code}")
            print(f"    Has links: {has_links}")
            
        except Exception as e:
            print(f"  ❌ Error reading {pattern_file}: {e}")

analyze_pattern_catalog()
```

### Task 4: Documentation Accessibility Verification

Check documentation accessibility and navigation:

```python
# Documentation accessibility analysis
def analyze_documentation_accessibility():
    """Analyze documentation accessibility and navigation"""
    
    print("=== DOCUMENTATION ACCESSIBILITY VERIFICATION ===")
    
    import os
    import glob
    
    # Check for main navigation files
    navigation_files = [
        "docs/NAVIGATION.md",
        "docs/README.md", 
        "docs/index.md",
        "README.md",
        "docs/TABLE_OF_CONTENTS.md"
    ]
    
    print("📖 Main navigation files:")
    for nav_file in navigation_files:
        if os.path.exists(nav_file):
            with open(nav_file, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = len(content.split('\n'))
                links = content.count('](')
            
            print(f"  ✅ {nav_file}: {lines} lines, {links} links")
        else:
            print(f"  ❌ {nav_file}: Not found")
    
    # Analyze directory-level documentation
    print(f"\n📁 Directory-level documentation:")
    
    for root, dirs, files in os.walk('docs'):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        level = root.replace('docs', '').count(os.sep)
        if level <= 2:  # Only check first 2 levels
            readme_exists = 'README.md' in files
            index_exists = any(f.startswith('index') for f in files)
            
            indent = '  ' * level
            marker = '✅' if (readme_exists or index_exists) else '❌'
            
            print(f"{indent}{marker} {root}: README={readme_exists}, Index={index_exists}")
    
    # Check for broken internal links in navigation
    print(f"\n🔗 Navigation link verification:")
    
    main_readme = "README.md"
    if os.path.exists(main_readme):
        with open(main_readme, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find markdown links
        import re
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        
        internal_md_links = [link for text, link in links if link.endswith('.md') and not link.startswith('http')]
        
        print(f"  Internal markdown links in README: {len(internal_md_links)}")
        
        # Check first few links
        for text, link in links[:5]:
            if link.endswith('.md') and not link.startswith('http'):
                exists = os.path.exists(link)
                marker = '✅' if exists else '❌'
                print(f"    {marker} {link}")
    
    # Check documentation categories
    print(f"\n📚 Documentation categories:")
    
    categories = [
        'architecture',
        'patterns', 
        'operations',
        'integration', 
        'internal',
        'api',
        'guides'
    ]
    
    for category in categories:
        category_dirs = glob.glob(f"docs/**/{category}*", recursive=True)
        category_files = glob.glob(f"docs/**/{category}*.md", recursive=True)
        
        total_items = len(category_dirs) + len(category_files)
        
        if total_items > 0:
            print(f"  ✅ {category}: {len(category_dirs)} dirs, {len(category_files)} files")
        else:
            print(f"  ❌ {category}: No dedicated documentation found")

analyze_documentation_accessibility()
```

### Task 5: GREAT-2 Documentation Impact Assessment

Assess documentation changes from recent GREAT-2 work:

```bash
# GREAT-2 documentation impact analysis
echo "=== GREAT-2 DOCUMENTATION IMPACT ASSESSMENT ==="

echo "📅 Recent documentation changes:"

# Check recent modifications (last 7 days)
echo "Documentation files modified in last 7 days:"
find docs/ -name "*.md" -mtime -7 2>/dev/null | wc -l

echo "Root documentation files modified in last 7 days:"
find . -maxdepth 1 -name "*.md" -mtime -7 2>/dev/null | wc -l

# Check for GREAT-2 specific documentation
echo ""
echo "🎯 GREAT-2 specific documentation:"

echo "Files mentioning GREAT-2:"
grep -r "GREAT-2" docs/ 2>/dev/null | cut -d: -f1 | sort -u | wc -l

echo "Files mentioning spatial patterns:"
grep -r "spatial.*pattern\|pattern.*spatial" docs/ 2>/dev/null | cut -d: -f1 | sort -u | wc -l

echo "Files mentioning ADR-038:"
grep -r "ADR-038\|adr-038" docs/ 2>/dev/null | cut -d: -f1 | sort -u | wc -l

echo "Files mentioning configuration validation:"
grep -r "configuration.*validation\|config.*validation" docs/ 2>/dev/null | cut -d: -f1 | sort -u | wc -l

# Check for documentation TODOs or incomplete items
echo ""
echo "⚠️ Documentation completeness check:"

echo "TODO items in documentation:"
grep -r "TODO\|FIXME\|TBD" docs/ 2>/dev/null | wc -l

echo "Placeholder content:"
grep -r "placeholder\|TODO\|coming soon" docs/ 2>/dev/null | wc -l

echo "Empty sections:"
grep -r "^## .*$" docs/ -A1 2>/dev/null | grep -c "^--$"

# Check specific files mentioned in GREAT-2E scope
echo ""
echo "📋 GREAT-2E scope verification:"

echo "Excellence Flywheel documentation:"
find docs/ -name "*excellence*" -o -name "*flywheel*" | wc -l

echo "Integration guides:"
find docs/ -name "*integration*guide*" -o -path "*integration*" -name "*guide*" | wc -l

echo "Pattern catalog files:"
find docs/ -name "*pattern*catalog*" -o -name "*catalog*pattern*" | wc -l
```

## Success Criteria

Phase 0 complete when:
- [✅] Documentation structure comprehensively mapped
- [✅] Link organization patterns analyzed
- [✅] Pattern catalog completeness verified
- [✅] Documentation accessibility assessed
- [✅] GREAT-2 documentation impact evaluated
- [✅] Remaining work scope clearly identified

---

**Your Mission**: Conduct comprehensive documentation organization analysis to determine exact scope of remaining work and coordination needs for GREAT-2E completion.

**Quality Standard**: Thorough documentation ecosystem analysis enabling efficient completion planning and coordination with Code agent findings.
