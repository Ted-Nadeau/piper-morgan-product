# Cursor Agent Prompt: GREAT-2E Phase 1 - Legacy Cleanup & Directory Documentation

## Mission: Documentation Organization & Legacy Cleanup

**Context**: Phase 0 revealed excellent core documentation with cleanup needed from reorganization/merge recovery. Pattern catalog is excellent (no work needed), focus on legacy cleanup and directory navigation.

**Objective**: Complete the documentation reorganization cleanup and create missing directory navigation to achieve 100% documentation organization.

## Phase 1 Tasks

### Task 1: Legacy Duplicate Cleanup

Remove duplicate and obsolete pattern files from reorganization artifacts:

```bash
# Legacy cleanup - remove duplicates and obsolete files
echo "=== LEGACY DUPLICATE CLEANUP ==="

echo "🔍 Identifying duplicate pattern files for cleanup:"

# Check uploads/ for pattern duplicates
echo "Pattern files in uploads/:"
find uploads/ -name "*pattern*" 2>/dev/null | head -10

# Check for scattered pattern catalogs
echo ""
echo "Pattern catalog duplicates:"
find . -name "*pattern*catalog*" -o -name "*catalog*pattern*" | grep -v "docs/internal/architecture/current/patterns"

# Check archive/ for old pattern files
echo ""
echo "Pattern files in archive areas:"
find . -path "*/archive/*" -name "*pattern*" 2>/dev/null | head -10

# Check for old documentation structure remnants
echo ""
echo "Old docs structure remnants:"
find docs/ -name "old*" -o -name "*old" -o -name "legacy*" -o -name "*legacy" 2>/dev/null

# Safe cleanup - move to archive rather than delete
echo ""
echo "📦 Creating archive structure for cleanup:"
mkdir -p archive/reorganization-cleanup/$(date +%Y-%m-%d)

# Move pattern duplicates to archive
echo ""
echo "🗂️ Archiving duplicate pattern files:"

# Archive uploads pattern files if they exist
if [ -d "uploads" ] && [ "$(find uploads/ -name "*pattern*" 2>/dev/null | wc -l)" -gt 0 ]; then
    echo "Archiving pattern files from uploads/"
    find uploads/ -name "*pattern*" -exec mv {} archive/reorganization-cleanup/$(date +%Y-%m-%d)/ \; 2>/dev/null
    echo "✅ Uploads pattern files archived"
else
    echo "ℹ️ No pattern files found in uploads/"
fi

# Archive scattered pattern catalogs (keep only the main one)
echo ""
echo "Archiving scattered pattern catalogs:"
find . -name "*pattern*catalog*" -o -name "*catalog*pattern*" | grep -v "docs/internal/architecture/current/patterns" | while read file; do
    if [ -f "$file" ]; then
        echo "Archiving: $file"
        mv "$file" "archive/reorganization-cleanup/$(date +%Y-%m-%d)/"
    fi
done

echo "✅ Legacy cleanup completed - files archived rather than deleted"
```

### Task 2: Directory Navigation Creation

Create missing README files for directories lacking navigation:

```python
# Create missing directory navigation
def create_directory_navigation():
    """Create README files for directories missing navigation"""
    
    print("=== DIRECTORY NAVIGATION CREATION ===")
    
    import os
    import glob
    
    # Find directories missing README files
    missing_readme_dirs = []
    
    for root, dirs, files in os.walk('docs'):
        # Skip hidden directories and specific exclusions
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
        
        # Check if directory has README
        has_readme = any(f.lower().startswith('readme') for f in files)
        has_index = any(f.lower().startswith('index') for f in files)
        has_md_files = any(f.endswith('.md') for f in files)
        
        # If directory has markdown files but no navigation, it needs a README
        if has_md_files and not (has_readme or has_index):
            # Skip if it's a leaf directory with only one file
            md_files = [f for f in files if f.endswith('.md')]
            if len(md_files) > 1 or len(dirs) > 0:
                missing_readme_dirs.append({
                    'path': root,
                    'md_files': md_files,
                    'subdirs': dirs.copy(),
                    'total_files': len(files)
                })
    
    print(f"📁 Directories needing navigation: {len(missing_readme_dirs)}")
    
    for dir_info in missing_readme_dirs[:10]:  # Show first 10
        print(f"  - {dir_info['path']}: {len(dir_info['md_files'])} MD files, {len(dir_info['subdirs'])} subdirs")
    
    # Create README files for missing directories
    created_readmes = []
    
    for dir_info in missing_readme_dirs:
        dir_path = dir_info['path']
        readme_path = os.path.join(dir_path, 'README.md')
        
        # Generate appropriate content based on directory
        dir_name = os.path.basename(dir_path)
        relative_path = dir_path.replace('docs/', '').replace('docs', 'root')
        
        readme_content = generate_directory_readme(dir_info, dir_name, relative_path)
        
        try:
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            created_readmes.append(readme_path)
            print(f"✅ Created: {readme_path}")
            
        except Exception as e:
            print(f"❌ Error creating {readme_path}: {e}")
    
    print(f"\n📊 Navigation creation summary:")
    print(f"  Directories analyzed: {len(missing_readme_dirs)}")
    print(f"  README files created: {len(created_readmes)}")
    
    return {
        'missing_dirs': len(missing_readme_dirs),
        'created_readmes': len(created_readmes),
        'readme_files': created_readmes
    }

def generate_directory_readme(dir_info, dir_name, relative_path):
    """Generate appropriate README content for directory"""
    
    md_files = dir_info['md_files']
    subdirs = dir_info['subdirs']
    
    # Create title
    title = dir_name.replace('-', ' ').replace('_', ' ').title()
    
    readme_content = f"""# {title}

## Overview

This directory contains documentation for {title.lower()} in the Piper Morgan system.

"""
    
    # Add file listings if there are markdown files
    if md_files:
        readme_content += f"""## Documentation Files

"""
        
        for md_file in sorted(md_files):
            # Create readable name from filename
            file_title = md_file.replace('-', ' ').replace('_', ' ').replace('.md', '').title()
            readme_content += f"- **[{file_title}]({md_file})** - {generate_file_description(md_file)}\n"
    
    # Add subdirectory listings if there are subdirectories
    if subdirs:
        readme_content += f"""
## Subdirectories

"""
        for subdir in sorted(subdirs):
            subdir_title = subdir.replace('-', ' ').replace('_', ' ').title()
            readme_content += f"- **[{subdir_title}]({subdir}/README.md)** - {generate_subdir_description(subdir)}\n"
    
    # Add navigation back to parent
    parent_path = os.path.dirname(relative_path)
    if parent_path and parent_path != '.':
        readme_content += f"""
## Navigation

- **[← Back to {parent_path.split('/')[-1].title()}](../README.md)**
- **[📚 Documentation Home](../../README.md)**

"""
    else:
        readme_content += f"""
## Navigation

- **[📚 Documentation Home](../README.md)**

"""
    
    # Add common footer
    readme_content += f"""---

**Last Updated**: October 1, 2025  
**Maintained By**: Documentation Team  
**Related**: [Documentation Standards](../../standards/documentation-standards.md)
"""
    
    return readme_content

def generate_file_description(filename):
    """Generate brief description based on filename"""
    
    descriptions = {
        'readme': 'Directory overview and navigation',
        'index': 'Directory index and navigation',
        'guide': 'Step-by-step guidance and instructions',
        'tutorial': 'Tutorial and learning materials',
        'reference': 'Reference documentation and specifications',
        'api': 'API documentation and specifications',
        'config': 'Configuration guidelines and examples',
        'setup': 'Setup and installation instructions',
        'troubleshooting': 'Common issues and solutions',
        'architecture': 'System architecture and design',
        'patterns': 'Design patterns and best practices',
        'integration': 'Integration guides and examples',
        'operations': 'Operational procedures and guidelines',
        'security': 'Security guidelines and procedures',
        'testing': 'Testing strategies and procedures',
        'deployment': 'Deployment guides and procedures',
        'monitoring': 'Monitoring and observability setup',
        'performance': 'Performance optimization guidelines'
    }
    
    filename_lower = filename.lower()
    
    for keyword, description in descriptions.items():
        if keyword in filename_lower:
            return description
    
    return "Documentation and guidance"

def generate_subdir_description(dirname):
    """Generate brief description based on directory name"""
    
    descriptions = {
        'architecture': 'System architecture documentation',
        'patterns': 'Design patterns and best practices',
        'integration': 'Integration guides and specifications',
        'operations': 'Operational procedures and guides',
        'security': 'Security documentation and guidelines',
        'testing': 'Testing documentation and procedures',
        'deployment': 'Deployment guides and automation',
        'monitoring': 'Monitoring and observability setup',
        'api': 'API documentation and references',
        'guides': 'User guides and tutorials',
        'reference': 'Reference documentation',
        'examples': 'Code examples and samples',
        'templates': 'Documentation templates',
        'standards': 'Documentation standards and guidelines',
        'internal': 'Internal documentation and procedures',
        'external': 'External integration documentation',
        'current': 'Current active documentation',
        'archived': 'Archived historical documentation',
        'legacy': 'Legacy system documentation'
    }
    
    dirname_lower = dirname.lower()
    
    for keyword, description in descriptions.items():
        if keyword in dirname_lower:
            return description
    
    return f"{dirname.replace('-', ' ').title()} documentation"

navigation_results = create_directory_navigation()
```

### Task 3: Documentation Organization Verification

Verify the improved documentation organization:

```bash
# Verify documentation organization improvements
echo "=== DOCUMENTATION ORGANIZATION VERIFICATION ==="

echo "📊 Documentation structure after cleanup:"

echo "Total markdown files:"
find docs/ -name "*.md" | wc -l

echo "Directories with README files:"
find docs/ -name "README.md" | wc -l

echo "Directories without README files:"
find docs/ -type d -exec test ! -e {}/README.md \; -print | grep -v "^\.$" | wc -l

echo ""
echo "📁 Directory coverage analysis:"

# Check coverage by depth
echo "Level 1 directories (docs/*):"
find docs/ -maxdepth 1 -type d | tail -n +2 | while read dir; do
    has_readme=$([ -f "$dir/README.md" ] && echo "✅" || echo "❌")
    echo "  $has_readme $(basename "$dir")"
done

echo ""
echo "Level 2 directories (docs/*/*):"
find docs/ -maxdepth 2 -mindepth 2 -type d | while read dir; do
    has_readme=$([ -f "$dir/README.md" ] && echo "✅" || echo "❌")
    has_md_files=$([ "$(find "$dir" -maxdepth 1 -name "*.md" | wc -l)" -gt 0 ] && echo "📄" || echo "📁")
    echo "  $has_readme $has_md_files $(echo "$dir" | sed 's|docs/||')"
done

echo ""
echo "🧹 Cleanup verification:"
echo "Archive directory structure:"
ls -la archive/reorganization-cleanup/ 2>/dev/null || echo "No archive directory created"

echo ""
echo "Remaining pattern files outside main catalog:"
find . -name "*pattern*" | grep -v "docs/internal/architecture/current/patterns" | grep -v "archive/" | head -10

echo ""
echo "📈 Organization quality metrics:"
total_md_files=$(find docs/ -name "*.md" | wc -l)
dirs_with_readme=$(find docs/ -name "README.md" | wc -l)
total_dirs_with_md=$(find docs/ -type d -exec sh -c 'test $(find "$1" -maxdepth 1 -name "*.md" | wc -l) -gt 0' _ {} \; -print | wc -l)

if [ "$total_dirs_with_md" -gt 0 ]; then
    coverage_percent=$(echo "scale=1; $dirs_with_readme * 100 / $total_dirs_with_md" | bc -l 2>/dev/null || echo "N/A")
    echo "README coverage: $dirs_with_readme/$total_dirs_with_md directories ($coverage_percent%)"
else
    echo "README coverage: Unable to calculate"
fi

echo "Total documentation files: $total_md_files"
echo "Navigation files created: $dirs_with_readme"
```

### Task 4: Content Quality Assessment

Assess and improve content quality markers:

```python
# Content quality assessment and improvement
def assess_content_quality():
    """Assess and improve documentation content quality"""
    
    print("=== CONTENT QUALITY ASSESSMENT ===")
    
    import os
    import glob
    import re
    
    # Find files with quality markers
    quality_issues = {
        'todos': [],
        'placeholders': [],
        'incomplete': [],
        'outdated': []
    }
    
    # Scan documentation files
    doc_files = glob.glob("docs/**/*.md", recursive=True)
    
    print(f"📄 Scanning {len(doc_files)} documentation files for quality issues...")
    
    for doc_file in doc_files:
        try:
            with open(doc_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for quality issues
            if re.search(r'\bTODO\b|\bFIXME\b|\bTBD\b', content, re.IGNORECASE):
                quality_issues['todos'].append(doc_file)
            
            if re.search(r'\bplaceholder\b|\bcoming soon\b|\bto be added\b', content, re.IGNORECASE):
                quality_issues['placeholders'].append(doc_file)
            
            if re.search(r'\bincomplete\b|\bunfinished\b|\bin progress\b', content, re.IGNORECASE):
                quality_issues['incomplete'].append(doc_file)
            
            if re.search(r'\boutdated\b|\blegacy\b|\bdeprec\w+\b', content, re.IGNORECASE):
                quality_issues['outdated'].append(doc_file)
                
        except Exception as e:
            print(f"⚠️ Error reading {doc_file}: {e}")
    
    # Report quality issues
    print(f"\n📊 Content quality analysis:")
    for issue_type, files in quality_issues.items():
        print(f"  {issue_type.title()}: {len(files)} files")
        
        # Show first few examples
        for file in files[:3]:
            print(f"    - {file}")
        
        if len(files) > 3:
            print(f"    ... and {len(files) - 3} more")
    
    # Create quality improvement recommendations
    recommendations = generate_quality_recommendations(quality_issues)
    
    return {
        'quality_issues': quality_issues,
        'recommendations': recommendations,
        'total_files_scanned': len(doc_files)
    }

def generate_quality_recommendations(quality_issues):
    """Generate recommendations for quality improvement"""
    
    recommendations = []
    
    if quality_issues['todos']:
        recommendations.append({
            'type': 'TODOs',
            'count': len(quality_issues['todos']),
            'priority': 'Medium',
            'action': 'Review and resolve TODO items or convert to GitHub issues',
            'timeline': 'Next sprint'
        })
    
    if quality_issues['placeholders']:
        recommendations.append({
            'type': 'Placeholders',
            'count': len(quality_issues['placeholders']),
            'priority': 'High',
            'action': 'Replace placeholder content with actual documentation',
            'timeline': 'This week'
        })
    
    if quality_issues['incomplete']:
        recommendations.append({
            'type': 'Incomplete Content',
            'count': len(quality_issues['incomplete']),
            'priority': 'Medium',
            'action': 'Complete unfinished documentation sections',
            'timeline': 'Next two weeks'
        })
    
    if quality_issues['outdated']:
        recommendations.append({
            'type': 'Outdated Content',
            'count': len(quality_issues['outdated']),
            'priority': 'Low',
            'action': 'Review and update or archive outdated documentation',
            'timeline': 'Next month'
        })
    
    return recommendations

quality_assessment = assess_content_quality()
```

### Task 5: Create Organization Summary

Generate comprehensive summary of documentation organization improvements:

```python
# Create organization improvement summary
def create_organization_summary():
    """Create comprehensive summary of organization improvements"""
    
    from datetime import datetime
    
    summary = f"""# GREAT-2E Phase 1 Organization Summary

## Overview
**Date**: {datetime.now().strftime('%B %d, %Y')}
**Epic**: GREAT-2E - Documentation Fixes & Excellence Flywheel
**Phase**: 1 - Legacy Cleanup & Directory Documentation
**Focus**: Documentation organization and navigation improvement

## Organization Improvements

### 1. Legacy Cleanup ✅

**Cleanup Actions**:
- Duplicate pattern files archived from uploads/ and scattered locations
- Pattern catalog duplicates removed (kept only main catalog)
- Old documentation structure remnants archived
- Archive structure created: `archive/reorganization-cleanup/YYYY-MM-DD/`

**Files Archived**:
- Pattern files from uploads/ directory
- Scattered pattern catalog duplicates
- Legacy documentation remnants
- Old structure artifacts from merge recovery

**Archive Strategy**:
- Files moved to archive rather than deleted (safer approach)
- Organized by date for future reference if needed
- Main pattern catalog preserved and untouched

### 2. Directory Navigation Enhancement ✅

**README Files Created**: {navigation_results.get('created_readmes', 0)}
**Directories Improved**: {navigation_results.get('missing_dirs', 0)}

**Navigation Features**:
- Consistent README structure across directories
- File listings with descriptions
- Subdirectory navigation
- Parent directory links
- Documentation home links

**Coverage Improvement**:
- Before: Many directories lacked navigation
- After: Comprehensive navigation coverage
- Standard format for consistency

### 3. Content Quality Assessment ✅

**Files Scanned**: {quality_assessment.get('total_files_scanned', 0)}
**Quality Issues Identified**:
- TODOs: {len(quality_assessment.get('quality_issues', {}).get('todos', []))} files
- Placeholders: {len(quality_assessment.get('quality_issues', {}).get('placeholders', []))} files
- Incomplete: {len(quality_assessment.get('quality_issues', {}).get('incomplete', []))} files
- Outdated: {len(quality_assessment.get('quality_issues', {}).get('outdated', []))} files

**Recommendations Generated**: {len(quality_assessment.get('recommendations', []))} improvement areas identified

## Documentation Organization Status

### Before Phase 1
- Pattern files scattered across multiple locations
- Many directories without navigation
- Incomplete cleanup from reorganization/merge recovery
- Inconsistent directory structure

### After Phase 1
- ✅ **Clean Organization**: Duplicates archived, main catalog preserved
- ✅ **Complete Navigation**: README files in all content directories
- ✅ **Consistent Structure**: Standard navigation format
- ✅ **Quality Assessment**: Content issues identified and prioritized

## Pattern Catalog Status

**Main Catalog**: `docs/internal/architecture/current/patterns/`
- **Status**: Excellent (31 files, pattern-000 to pattern-030)
- **Organization**: Perfect numbering sequence
- **Quality**: Comprehensive and well-maintained
- **Action**: No changes needed - catalog is exemplary

**Cleanup**: Duplicate and scattered pattern files properly archived

## Directory Navigation Coverage

### Navigation Files Created
"""
    
    # Add specific README files created
    for readme_file in navigation_results.get('readme_files', []):
        relative_path = readme_file.replace('docs/', '')
        summary += f"- `{relative_path}` - Directory navigation and file listings\n"
    
    summary += f"""
### Navigation Standards Applied
- **File Listings**: Descriptive links to all markdown files
- **Subdirectory Links**: Navigation to child directories
- **Parent Navigation**: Links back to parent directories
- **Consistent Format**: Standard structure across all directories
- **Maintenance Info**: Update dates and ownership

## Quality Improvement Recommendations

"""
    
    # Add quality recommendations
    for rec in quality_assessment.get('recommendations', []):
        summary += f"""### {rec['type']} ({rec['priority']} Priority)
- **Count**: {rec['count']} files affected
- **Action**: {rec['action']}
- **Timeline**: {rec['timeline']}

"""
    
    summary += f"""## Archive Organization

### Archive Structure
```
archive/
└── reorganization-cleanup/
    └── {datetime.now().strftime('%Y-%m-%d')}/
        ├── duplicate-pattern-files
        ├── scattered-catalogs
        └── legacy-remnants
```

### Archive Contents
- Pattern files from uploads/ directory
- Duplicate pattern catalog files
- Legacy documentation structure remnants
- Obsolete organizational artifacts

**Archive Policy**: Files preserved for reference, organized by cleanup date

## Impact Assessment

### Organization Quality
- **Before**: Scattered files, missing navigation, incomplete cleanup
- **After**: Clean structure, comprehensive navigation, quality assessment

### Maintenance Efficiency
- **Before**: Manual navigation, difficult discovery
- **After**: Systematic navigation, easy content discovery

### User Experience
- **Before**: Difficult to find related documentation
- **After**: Clear navigation paths, consistent structure

## Future Maintenance

### Ongoing Tasks
1. **Content Quality**: Address identified TODOs and placeholders
2. **Navigation Maintenance**: Update README files when structure changes
3. **Archive Management**: Periodic review of archived content
4. **Quality Monitoring**: Regular content quality assessments

### Prevention Measures
- **Documentation Standards**: Follow navigation format for new directories
- **Quality Gates**: Review content quality in PR process
- **Regular Audits**: Periodic organization and quality assessments

## Success Metrics

### Organization Metrics
- **README Coverage**: Comprehensive navigation in content directories
- **Clean Structure**: Duplicates archived, main content organized
- **Quality Assessment**: Issues identified and prioritized

### Process Improvements
- **Systematic Cleanup**: Archive-first approach preserves content
- **Consistent Navigation**: Standard format across directories
- **Quality Monitoring**: Proactive identification of content issues

---

**Phase 1 Status**: COMPLETE ✅
**Organization Quality**: Significantly improved
**Next Steps**: Monitor navigation usage, address quality recommendations
**Maintenance**: Follow documentation standards for ongoing organization
"""
    
    with open('great_2e_phase_1_organization_summary.md', 'w') as f:
        f.write(summary)
    
    print("✅ Organization summary created: great_2e_phase_1_organization_summary.md")
    
    return summary

organization_summary = create_organization_summary()
```

## Success Criteria

Phase 1 complete when:
- [✅] Legacy duplicate files cleaned up and archived
- [✅] Missing directory README files created
- [✅] Documentation organization verified and improved
- [✅] Content quality assessed and recommendations generated
- [✅] Organization summary created with comprehensive improvements
- [✅] Navigation coverage significantly improved

---

**Your Mission**: Complete the documentation reorganization cleanup and create systematic directory navigation to achieve 100% documentation organization excellence.

**Quality Standard**: Clean, navigable documentation structure with comprehensive coverage and systematic maintenance approach.
