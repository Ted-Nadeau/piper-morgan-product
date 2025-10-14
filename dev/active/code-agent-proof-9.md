# Code Agent Prompt: PROOF-9 - Documentation Sync Process

**Date**: October 13, 2025, 6:32 PM
**Phase**: PROOF-9 (Documentation Sync Process)
**Duration**: 2-3 hours estimated, **20-40 min actual** (based on efficiency gains)
**Priority**: HIGH (Completes Stage 2!)
**Agent**: Code Agent

---

## CRITICAL CORRECTION

**EXISTING SYSTEMS** (Do NOT recreate):
1. ✅ **Weekly Audit Process** - `.github/workflows/weekly-docs-audit.yml` exists and runs Mondays
2. ✅ **Pre-commit Hooks** - Already exist in repository
3. ✅ **Weekly Sweep** - Code agent ran it today (session log: `2025-10-13-0920-docs-code-log.md`)

**ACTUAL TASK**: Review existing systems, improve if needed, create missing metrics script

---

## Mission

Review and improve existing documentation sync systems. Create automated metrics script (the missing piece). Document the complete sync infrastructure.

**Goal**: Make existing sync systems better, not recreate the wheel.

---

## Critical Reminder: Post-Compaction Protocol

**AFTER ANY COMPACTION/SUMMARY**:
1. ✅ Re-verify the actual assignment before concluding
2. ✅ Review what EXISTS before creating
3. ✅ Improve existing systems, don't duplicate
4. ✅ Complete the assigned work fully

**Assignment**: Review existing systems + create metrics script + document complete sync process

---

## System 1: Review Existing Weekly Audit (10 minutes)

### Find and Review the Workflow

**File**: `.github/workflows/weekly-docs-audit.yml` (exists!)

**From session log today**, this workflow:
- Runs every Monday
- Creates issue #238 for weekly sweep
- Was just updated today with 4 corrections
- Includes CITATIONS.md review, README review, meta/recursive improvement

**Tasks**:
1. **Read the workflow file**:
   ```bash
   cat .github/workflows/weekly-docs-audit.yml
   ```

2. **Assess completeness**:
   - Does it check documentation drift?
   - Does it verify metrics?
   - Does it create actionable issues?
   - Is the checklist comprehensive?

3. **Suggest improvements** (if any):
   - Missing checks?
   - Better automation possible?
   - More actionable output?

**Output**: Brief assessment in completion report

---

## System 2: Review Existing Pre-Commit Hooks (10 minutes)

### Find and Review Hooks

**Likely locations**:
- `.git/hooks/pre-commit`
- `scripts/git-hooks/` (template location)
- `.husky/` (if using husky)

**Tasks**:
1. **Find existing hooks**:
   ```bash
   ls -la .git/hooks/
   cat .git/hooks/pre-commit 2>/dev/null || echo "No pre-commit hook found"

   # Check for templates/scripts
   find . -name "*pre-commit*" -not -path "./usr/*" -not -path "./home/*"
   ```

2. **Assess what they do**:
   - Warn about code without docs?
   - Check formatting?
   - Run tests?
   - Other quality gates?

3. **Suggest improvements** (if any):
   - Add documentation checks?
   - Better warnings?
   - More helpful output?

**Output**: Brief assessment in completion report

---

## System 3: Create Automated Metrics Script (15 minutes)

**This is the NEW piece to create** - automated metrics generation

### Create Metrics Update Script

**File**: `scripts/update_docs_metrics.py`

**Purpose**: Auto-generate metrics that documentation references

**Implementation** (streamlined for speed):
```python
#!/usr/bin/env python3
"""
Documentation Metrics Updater

Automatically updates docs/metrics.md with current codebase metrics.
Run this script when documentation needs refreshing.

Usage:
    python scripts/update_docs_metrics.py
"""

import subprocess
from pathlib import Path
from datetime import datetime

def count_tests() -> dict:
    """Count all test files and test functions."""
    try:
        # Quick count of test files
        test_files = list(Path('tests').rglob('test_*.py'))
        contract_tests = list(Path('tests/intent/contracts').glob('test_*.py')) if Path('tests/intent/contracts').exists() else []
        regression_tests = list(Path('tests/regression').glob('test_*.py')) if Path('tests/regression').exists() else []

        return {
            'test_files': len(test_files),
            'contract_tests': len(contract_tests),
            'regression_tests': len(regression_tests),
        }
    except Exception as e:
        return {'error': str(e)}

def count_lines() -> dict:
    """Count lines in key directories."""
    def count_in_dir(path: str) -> int:
        try:
            result = subprocess.run(
                f"find {path} -name '*.py' -exec wc -l {{}} + 2>/dev/null | tail -1",
                shell=True, capture_output=True, text=True
            )
            return int(result.stdout.split()[0]) if result.stdout else 0
        except:
            return 0

    return {
        'services': count_in_dir('services'),
        'tests': count_in_dir('tests'),
        'web': count_in_dir('web'),
        'cli': count_in_dir('cli'),
    }

def count_adrs() -> int:
    """Count ADRs."""
    try:
        adr_dir = Path('docs/internal/architecture/current/adrs')
        return len(list(adr_dir.glob('adr-*.md'))) if adr_dir.exists() else 0
    except:
        return 0

def count_plugins() -> list:
    """Count plugin implementations."""
    plugins = ['github', 'slack', 'notion', 'calendar']
    base = Path('services/integrations')
    return [p for p in plugins if (base / p).exists()] if base.exists() else []

def update_metrics_file(metrics: dict):
    """Write metrics to docs/metrics.md"""

    content = f"""# Piper Morgan Codebase Metrics

**Last Updated**: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
**Auto-Generated**: This file is automatically updated by `scripts/update_docs_metrics.py`

---

## Test Coverage

- **Test Files**: {metrics['tests']['test_files']}
- **Contract Tests**: {metrics['tests']['contract_tests']}
- **Regression Tests**: {metrics['tests']['regression_tests']}

---

## Codebase Size

- **Services**: {metrics['lines']['services']:,} lines
- **Tests**: {metrics['lines']['tests']:,} lines
- **Web**: {metrics['lines']['web']:,} lines
- **CLI**: {metrics['lines']['cli']:,} lines

---

## Architecture

- **ADRs**: {metrics['adrs']} architecture decision records

---

## Plugins

- **Operational**: {', '.join(metrics['plugins']) if metrics['plugins'] else 'None'}

---

## How to Update

```bash
python scripts/update_docs_metrics.py
```

*Do not manually edit this file - changes will be overwritten.*

---

*Generated by Documentation Sync Process (PROOF-9)*
"""

    Path('docs').mkdir(exist_ok=True)
    Path('docs/metrics.md').write_text(content)
    print(f"✅ Updated docs/metrics.md")

def main():
    """Main execution."""
    print("📊 Gathering metrics...")

    metrics = {
        'tests': count_tests(),
        'lines': count_lines(),
        'adrs': count_adrs(),
        'plugins': count_plugins(),
    }

    print(f"   Test Files: {metrics['tests'].get('test_files', 0)}")
    print(f"   Services: {metrics['lines']['services']:,} lines")
    print(f"   ADRs: {metrics['adrs']}")

    print("\n📝 Updating docs/metrics.md...")
    update_metrics_file(metrics)

    print("\n✅ Documentation metrics updated!")
    print("   Commit this file with your next documentation update.")

if __name__ == "__main__":
    main()
```

**Test the script**:
```bash
# Make executable
chmod +x scripts/update_docs_metrics.py

# Run it
python scripts/update_docs_metrics.py

# Verify output
cat docs/metrics.md
```

---

## Documentation Phase (10 minutes)

### Document the Complete Sync System

**File**: `docs/processes/documentation-sync-system.md`

**Purpose**: Explain how all the pieces work together

```markdown
# Documentation Sync System

**Established**: October 13, 2025 (PROOF-9)
**Purpose**: Prevent documentation drift through automated checks

---

## Three-Layer Defense System

### Layer 1: Pre-Commit Hooks (Immediate)
**Location**: `.git/hooks/pre-commit`
**Frequency**: Every commit
**Action**: Warns when code changes without doc updates

**What it does**:
- Detects changed code files
- Checks if documentation also changed
- Warns developer if docs not updated
- Allows commit (doesn't block)

### Layer 2: Weekly Audit (Regular)
**Location**: `.github/workflows/weekly-docs-audit.yml`
**Frequency**: Every Monday
**Action**: Creates issue #238 with comprehensive checklist

**What it includes**:
- Modified files review (past week)
- Infrastructure verification (ports, patterns, line counts)
- Quality checks (README freshness, backup files)
- CITATIONS.md completeness
- Metrics collection
- Meta/recursive improvements

**Duration**: 15-30 minutes
**Owner**: PM or designated team member

### Layer 3: Automated Metrics (On-Demand)
**Location**: `scripts/update_docs_metrics.py`
**Frequency**: As needed
**Action**: Generates `docs/metrics.md` with current stats

**What it tracks**:
- Test counts (files, contract, regression)
- Line counts (services, tests, web, cli)
- ADR count
- Plugin count

**Usage**:
```bash
python scripts/update_docs_metrics.py
```

---

## How They Work Together

1. **During Development** (Layer 1):
   - Pre-commit hook warns about missing doc updates
   - Developer remembers to update docs

2. **Weekly Check-In** (Layer 2):
   - GitHub Action creates audit issue every Monday
   - Team reviews past week's changes
   - Catches anything missed during development

3. **Documentation Updates** (Layer 3):
   - Run metrics script to get current numbers
   - Update documentation with verified metrics
   - Commit updated docs/metrics.md

---

## When to Do Full PROOF Work

- **Minor Drift** (<5% inaccuracy): Note for next quarterly review
- **Major Drift** (>10% inaccuracy): Create PROOF-style epic
- **Pattern of Drift**: Improve automation

---

## System Maintenance

**Monthly**:
- Review weekly audit findings
- Check if metrics script needs updates
- Verify pre-commit hooks still working

**Quarterly**:
- Full documentation accuracy audit
- Update automation scripts
- Improve checklists based on drift patterns

---

*Part of CORE-CRAFT-PROOF (Stage 2: Documentation)*
```

---

## Output Phase (5 minutes)

### Create PROOF-9 Completion Report

**File**: `dev/2025/10/13/proof-9-documentation-sync-completion.md`

**Structure**:
```markdown
# PROOF-9: Documentation Sync System Review & Enhancement

**Date**: October 13, 2025, 6:32 PM
**Agent**: Code Agent
**Duration**: [Actual time]

---

## Mission Accomplished

Reviewed existing sync systems and created missing metrics automation.

---

## Existing Systems Reviewed

### 1. Weekly Audit Workflow ✅
**File**: `.github/workflows/weekly-docs-audit.yml`
**Status**: Exists and operational (ran today)
**Last Updated**: October 13, 2025 (4 corrections applied)

**Assessment**:
- [Your assessment of completeness]
- [What it does well]
- [Any suggested improvements]

**Recent Improvements** (from today's session):
- Fixed CITATIONS.md filename reference
- Added ROOT README.md review
- Added meta/recursive improvement section
- Updated CLAUDE.md line counts

### 2. Pre-Commit Hooks ✅
**Location**: [Where found]
**Status**: [Assessment]

**Assessment**:
- [What hooks exist]
- [What they check]
- [Any suggested improvements]

---

## New System Created

### 3. Automated Metrics Script ✅
**File**: `scripts/update_docs_metrics.py` (NEW)
**Output**: `docs/metrics.md`

**Purpose**: Auto-generate verifiable metrics

**Metrics Tracked**:
- Test counts: [X] files
- Line counts: [X] services lines, etc.
- ADRs: [X]
- Plugins: [X]

**Testing**: [Results of running script]

---

## Complete Sync System Documentation

**File**: `docs/processes/documentation-sync-system.md` (NEW)

**Purpose**: Explain how all three layers work together

**Contents**:
- Three-layer defense explanation
- How systems complement each other
- When to escalate to full PROOF work
- Maintenance schedule

---

## Files Created/Modified

**New Files**:
- [x] scripts/update_docs_metrics.py
- [x] docs/metrics.md (generated)
- [x] docs/processes/documentation-sync-system.md
- [x] dev/2025/10/13/proof-9-documentation-sync-completion.md

**Review Only** (no changes needed):
- [x] .github/workflows/weekly-docs-audit.yml
- [x] .git/hooks/pre-commit (or wherever found)

**Total**: [X] new files, [X] reviews complete

---

## Stage 2 Complete! 🎉

**PROOF-9 completes Stage 2 (Documentation)**:
- ✅ PROOF-0: Reconnaissance (90 min)
- ✅ PROOF-1: GREAT-1 Docs (80 min → 99%+ accuracy)
- ✅ PROOF-3: GREAT-3 Docs (24 min → 99%+ accuracy)
- ✅ PROOF-8: ADR Completion (60 min → 95%+ complete)
- ✅ PROOF-9: Doc Sync System (XX min → automated)

**Total Stage 2**: ~4 hours actual vs 8-12 estimated (2-3x faster!)

---

**Completion Time**: [timestamp]
**Status**: PROOF-9 Complete ✅
**Stage 2 Status**: COMPLETE ✅
```

---

## Commit Strategy

```bash
# Stage new files only (don't change existing systems)
git add scripts/update_docs_metrics.py
git add docs/metrics.md
git add docs/processes/documentation-sync-system.md
git add dev/2025/10/13/proof-9-*.md

# Commit
git commit -m "feat(PROOF-9): Document and enhance documentation sync system

Reviewed existing sync infrastructure and added missing metrics automation.

Existing Systems (Reviewed, No Changes):
- Weekly audit workflow (.github/workflows/weekly-docs-audit.yml)
  - Runs every Monday, creates issue #238
  - Recently updated with 4 corrections (today)
- Pre-commit hooks (reviewed and documented)

New System Created:
- Automated metrics script (scripts/update_docs_metrics.py)
  - Generates docs/metrics.md with current stats
  - Tracks tests, lines, ADRs, plugins
  - On-demand updates for documentation

Documentation:
- Complete sync system documentation
- Three-layer defense strategy explained
- Maintenance and escalation guidelines

Result: Automated documentation sync without recreating existing systems

Part of: CORE-CRAFT-PROOF epic, Stage 2 (Documentation)
Completes: Stage 2 - Documentation track ✅"

# Push
git push origin main
```

---

## Success Criteria

### Reviews Complete ✅
- [ ] Weekly audit workflow reviewed
- [ ] Pre-commit hooks found and reviewed
- [ ] Assessment of existing systems documented

### New System Created ✅
- [ ] Metrics script functional
- [ ] Metrics script tested
- [ ] docs/metrics.md generated

### Documentation Complete ✅
- [ ] Sync system documented
- [ ] Three layers explained
- [ ] Completion report created

### Committed ✅
- [ ] New files staged
- [ ] Descriptive commit message
- [ ] Pushed to main

### Stage 2 Complete ✅
- [ ] All PROOF tasks done
- [ ] Documentation sync automated
- [ ] Ready for Stage 3

---

## Time Budget

**Revised Estimate** (review vs create):

**Optimistic**: 20 minutes
- Review weekly audit: 5 min
- Review hooks: 5 min
- Create metrics script: 10 min

**Realistic**: 30 minutes
- Review weekly audit: 8 min
- Review hooks: 7 min
- Create metrics script: 15 min

**Target Completion**: 7:00-7:05 PM

---

## What NOT to Do

- ❌ Don't recreate the weekly audit workflow
- ❌ Don't recreate pre-commit hooks
- ❌ Don't duplicate existing systems
- ❌ Don't make major changes to working systems

## What TO Do

- ✅ Review what exists
- ✅ Document existing systems
- ✅ Create only the missing piece (metrics)
- ✅ Suggest improvements (don't force them)
- ✅ Respect the wheel that's already invented

---

## Context

**PM Correction**: "They exist. The weekly audit is powered by a GitHub action. It ran today. Hold on... Similary, pre-commit hooks exist. We can ask Code to review and improve what's there but let us not reinvent the wheel?"

**Critical Learning**: Check what EXISTS before creating new systems!

**What This Actually Does**:
- Reviews existing weekly audit (just updated today!)
- Reviews existing pre-commit hooks
- Creates missing metrics script
- Documents how everything works together
- **Doesn't recreate the wheel** ✅

---

**PROOF-9 Start Time**: 6:35 PM
**Expected Completion**: 7:00-7:05 PM (20-30 minutes)
**PM Status**: At dinner, checking in at intervals

**LET'S REVIEW AND ENHANCE (NOT RECREATE)! 📚✅**

---

*"The best new system is an improved existing system."*
*- PROOF-9 (Corrected) Philosophy*

---

## Critical Reminder: Post-Compaction Protocol

**AFTER ANY COMPACTION/SUMMARY**:
1. ✅ Re-verify the actual assignment before concluding
2. ✅ If parts of the system not implemented, MUST IMPLEMENT THEM
3. ✅ Don't decide pieces are "optional" or "can be deferred"
4. ✅ Complete the assigned work fully

**Assignment**: Create ALL three sync systems (metrics script, git hooks, audit process)

---

## Context

### Why This Matters
**From PROOF-0 discoveries**:
- GREAT-2 claimed 20+ files, actually ~10 files
- GREAT-4 test count evolved 126→142 during work
- ADR-034 claimed 281 lines, actually 280
- Documentation drift is subtle but cumulative

**Root Cause**: No automated verification between code and documentation

**Solution**: Three-layer defense system

---

## System 1: Automated Metrics Script (20 minutes)

### Create Metrics Update Script

**File**: `scripts/update_docs_metrics.py`

**Purpose**: Auto-generate metrics that documentation references

**Implementation**:
```python
#!/usr/bin/env python3
"""
Documentation Metrics Updater

Automatically updates docs/metrics.md with current codebase metrics.
Run this script when documentation needs refreshing.

Usage:
    python scripts/update_docs_metrics.py
"""

import subprocess
from pathlib import Path
from datetime import datetime

def count_tests() -> dict:
    """Count all test files and test functions."""
    result = subprocess.run(
        ["pytest", "--collect-only", "-q"],
        capture_output=True,
        text=True
    )

    # Parse pytest output
    lines = result.stdout.split('\n')
    test_count = 0
    for line in lines:
        if 'test' in line.lower():
            test_count += 1

    # Count test files
    test_files = list(Path('tests').rglob('test_*.py'))

    return {
        'total_tests': test_count,
        'test_files': len(test_files),
        'contract_tests': len(list(Path('tests/intent/contracts').glob('*.py'))),
        'regression_tests': len(list(Path('tests/regression').glob('*.py'))),
    }

def count_lines() -> dict:
    """Count lines in key directories."""
    def count_in_dir(path: str, pattern: str = "*.py") -> int:
        files = Path(path).rglob(pattern)
        total = 0
        for f in files:
            try:
                total += len(f.read_text().split('\n'))
            except:
                pass
        return total

    return {
        'services': count_in_dir('services'),
        'tests': count_in_dir('tests'),
        'web': count_in_dir('web'),
        'cli': count_in_dir('cli'),
        'total_python': count_in_dir('.', '*.py'),
    }

def count_adrs() -> dict:
    """Count ADRs and their status."""
    adr_dir = Path('docs/internal/architecture/current/adrs')
    adrs = list(adr_dir.glob('adr-*.md'))

    return {
        'total_adrs': len(adrs),
        'adr_directory': str(adr_dir),
    }

def count_plugins() -> dict:
    """Count plugin implementations."""
    plugins = [
        'services/integrations/github',
        'services/integrations/slack',
        'services/integrations/notion',
        'services/integrations/calendar',
    ]

    operational = []
    for plugin in plugins:
        if Path(plugin).exists():
            operational.append(Path(plugin).name)

    return {
        'total_plugins': len(operational),
        'operational_plugins': operational,
    }

def update_metrics_file(metrics: dict):
    """Write metrics to docs/metrics.md"""

    content = f"""# Piper Morgan Codebase Metrics

**Last Updated**: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
**Auto-Generated**: This file is automatically updated by `scripts/update_docs_metrics.py`

---

## Test Coverage

- **Total Tests**: {metrics['tests']['total_tests']}
- **Test Files**: {metrics['tests']['test_files']}
- **Contract Tests**: {metrics['tests']['contract_tests']}
- **Regression Tests**: {metrics['tests']['regression_tests']}

---

## Codebase Size

- **Services**: {metrics['lines']['services']:,} lines
- **Tests**: {metrics['lines']['tests']:,} lines
- **Web**: {metrics['lines']['web']:,} lines
- **CLI**: {metrics['lines']['cli']:,} lines
- **Total Python**: {metrics['lines']['total_python']:,} lines

---

## Architecture

- **ADRs**: {metrics['adrs']['total_adrs']} architecture decision records
- **ADR Location**: `{metrics['adrs']['adr_directory']}`

---

## Plugins

- **Total Plugins**: {metrics['plugins']['total_plugins']}
- **Operational**: {', '.join(metrics['plugins']['operational_plugins'])}

---

## How to Update

This file is automatically generated. To update:

```bash
python scripts/update_docs_metrics.py
```

Do not manually edit this file - changes will be overwritten.

---

*Generated by Documentation Sync Process (PROOF-9)*
"""

    Path('docs/metrics.md').write_text(content)
    print(f"✅ Updated docs/metrics.md")

def main():
    """Main execution."""
    print("📊 Gathering metrics...")

    metrics = {
        'tests': count_tests(),
        'lines': count_lines(),
        'adrs': count_adrs(),
        'plugins': count_plugins(),
    }

    print(f"   Tests: {metrics['tests']['total_tests']}")
    print(f"   Lines: {metrics['lines']['total_python']:,}")
    print(f"   ADRs: {metrics['adrs']['total_adrs']}")
    print(f"   Plugins: {metrics['plugins']['total_plugins']}")

    print("\n📝 Updating docs/metrics.md...")
    update_metrics_file(metrics)

    print("\n✅ Documentation metrics updated!")
    print("   File: docs/metrics.md")
    print("   Commit this file with your next documentation update.")

if __name__ == "__main__":
    main()
```

**Test the script**:
```bash
# Make executable
chmod +x scripts/update_docs_metrics.py

# Run it
python scripts/update_docs_metrics.py

# Verify output
cat docs/metrics.md
```

---

## System 2: Git Hooks (15 minutes)

### Create Pre-Commit Hook

**File**: `.git/hooks/pre-commit`

**Purpose**: Warn when code changes without doc updates

**Implementation**:
```bash
#!/bin/bash
# Pre-commit hook to check documentation sync

# Get list of changed files
CHANGED_FILES=$(git diff --cached --name-only)

# Check if any code files changed
CODE_CHANGED=false
if echo "$CHANGED_FILES" | grep -qE '\.(py)$'; then
    CODE_CHANGED=true
fi

# Check if any documentation files changed
DOCS_CHANGED=false
if echo "$CHANGED_FILES" | grep -qE '(\.md$|docs/)'; then
    DOCS_CHANGED=true
fi

# Check if services changed (usually needs doc updates)
SERVICES_CHANGED=false
if echo "$CHANGED_FILES" | grep -q 'services/'; then
    SERVICES_CHANGED=true
fi

# Warn if code changed but docs didn't
if [ "$CODE_CHANGED" = true ] && [ "$DOCS_CHANGED" = false ]; then
    echo "⚠️  WARNING: Code files changed but no documentation updated"
    echo ""
    echo "Changed code files:"
    echo "$CHANGED_FILES" | grep '\.py$' | sed 's/^/  - /'
    echo ""
    echo "Consider updating:"
    echo "  - docs/architecture/architecture.md (if architecture changed)"
    echo "  - docs/metrics.md (run: python scripts/update_docs_metrics.py)"
    echo "  - Relevant ADRs in docs/internal/architecture/current/adrs/"
    echo ""
    echo "To skip this check: git commit --no-verify"
    echo ""

    # Don't block commit, just warn
    # Uncomment next line to block commits:
    # exit 1
fi

# Special check for services changes
if [ "$SERVICES_CHANGED" = true ] && [ "$DOCS_CHANGED" = false ]; then
    echo "⚠️  WARNING: Services directory changed - documentation likely needs update"
    echo ""
fi

# Allow commit to proceed
exit 0
```

**Install the hook**:
```bash
# Make executable
chmod +x .git/hooks/pre-commit

# Test it (make a code change without doc change)
# It should warn but allow commit
```

**Note**: This hook is local to each developer's repo. To share with team, we could use `husky` or similar tool, but for now we document the process.

### Create Hook Installation Script

**File**: `scripts/install_git_hooks.sh`

**Purpose**: Make it easy to install hooks

**Implementation**:
```bash
#!/bin/bash
# Install git hooks for documentation sync

echo "📦 Installing git hooks..."

# Copy pre-commit hook
cp scripts/git-hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

echo "✅ Pre-commit hook installed"
echo "   Location: .git/hooks/pre-commit"
echo "   Purpose: Warns when code changes without doc updates"
echo ""
echo "To test: Make a code change and commit without updating docs"
```

**And the actual hook template**:

**File**: `scripts/git-hooks/pre-commit`

(Same content as above, but in a shareable location)

---

## System 3: Weekly Audit Process (10 minutes)

### Create Audit Process Documentation

**File**: `docs/processes/weekly-documentation-audit.md`

**Purpose**: Establish repeatable audit process

**Implementation**:
```markdown
# Weekly Documentation Audit Process

**Frequency**: Every Monday
**Duration**: 15-30 minutes
**Owner**: PM or designated team member

---

## Purpose

Catch documentation drift early before it accumulates. This is a lightweight check, not a full PROOF epic.

---

## Process

### 1. Run Automated Metrics (5 minutes)

```bash
# Update metrics
python scripts/update_docs_metrics.py

# Check git diff
git diff docs/metrics.md

# If changed significantly, note for review
```

### 2. Spot Check Recent Changes (10 minutes)

```bash
# See what code changed in last week
git log --since="1 week ago" --name-only --pretty=format: | sort -u | grep '\.py$'

# Check if corresponding docs updated
# Focus on:
# - services/ changes (check architecture.md)
# - New features (check relevant ADRs)
# - Performance changes (check metrics)
```

### 3. Quick Serena Verification (10 minutes)

Pick one GREAT epic to spot-check:

```bash
# Example: Verify GREAT-3 plugin count
# Expected: 4 plugins
# Actual: (check with Serena or ls services/integrations/)

# If mismatch: Create issue for PROOF work
```

### 4. Document Findings (5 minutes)

**File**: `docs/drift-log.md`

Add entry:
```markdown
## Week of [Date]

**Metrics Updated**: Yes/No
**Spot Checks**:
- [Epic/Component]: ✅ Accurate / ⚠️ Minor drift / ❌ Major drift

**Issues Created**: [List any issues]
**Time Spent**: [X] minutes
```

---

## When to Do Full PROOF Work

- **Minor Drift** (<5% inaccuracy): Note for next quarterly review
- **Major Drift** (>10% inaccuracy): Create PROOF-style epic
- **Pattern of Drift**: Improve automation (update scripts/hooks)

---

## Automation Ideas

Future improvements:
- GitHub Action to run metrics weekly
- Slack notification of drift
- Dashboard showing doc health
```

### Create Drift Log

**File**: `docs/drift-log.md`

**Purpose**: Track documentation accuracy over time

**Implementation**:
```markdown
# Documentation Drift Log

**Purpose**: Track documentation accuracy between PROOF audits

---

## Current Status (October 13, 2025)

**Last Full Audit**: PROOF epic (October 13, 2025)
**Accuracy**: 99%+
**Next Full Audit**: Q1 2026 (or when major drift detected)

---

## Week of October 13, 2025

**Metrics Updated**: Yes (PROOF-9)
**Spot Checks**:
- GREAT-1 (QueryRouter): ✅ 99%+ accurate (PROOF-1)
- GREAT-3 (Plugins): ✅ 99%+ accurate (PROOF-3)
- ADR Library: ✅ 95%+ complete (PROOF-8)

**Issues Created**: None
**Time Spent**: Full PROOF epic (Stage 2 complete)

**Notes**: Baseline established. Sync processes now in place.

---

## How to Use This Log

Each week, add a new section:

```markdown
## Week of [Date]

**Metrics Updated**: Yes/No
**Spot Checks**: [What you checked]
**Drift Detected**: None / Minor / Major
**Issues Created**: [Issue numbers]
**Time Spent**: [X] minutes
```

If drift is detected, investigate and fix before it accumulates.

---

*Established by PROOF-9 (October 13, 2025)*
```

---

## Verification Phase (10 minutes)

### Test All Three Systems

**1. Test Metrics Script**:
```bash
python scripts/update_docs_metrics.py
# Should create docs/metrics.md with current stats
# Verify numbers look reasonable
```

**2. Test Git Hook**:
```bash
# Make a small code change (e.g., add comment to a service file)
echo "# Test comment" >> services/orchestration/engine.py

# Try to commit without doc change
git add services/orchestration/engine.py
git commit -m "test: verify pre-commit hook"

# Should see warning but allow commit
# Then reset:
git reset HEAD~1
git checkout services/orchestration/engine.py
```

**3. Verify Audit Process**:
```bash
# Check files exist
ls docs/processes/weekly-documentation-audit.md
ls docs/drift-log.md

# Verify they're readable and complete
cat docs/processes/weekly-documentation-audit.md | wc -l
# Should be 50+ lines
```

---

## Output Phase (5 minutes)

### Create PROOF-9 Completion Report

**File**: `dev/2025/10/13/proof-9-documentation-sync-completion.md`

**Structure**:
```markdown
# PROOF-9: Documentation Sync Process

**Date**: October 13, 2025, 6:32 PM
**Agent**: Code Agent
**Duration**: [Actual time]

---

## Mission Accomplished

Established three-layer documentation sync system to prevent future drift.

---

## Systems Created

### 1. Automated Metrics Script ✅
**File**: `scripts/update_docs_metrics.py`
**Purpose**: Auto-generate codebase metrics
**Output**: `docs/metrics.md`

**Metrics Tracked**:
- Test counts (total, contract, regression)
- Line counts (services, tests, web, cli)
- ADR count
- Plugin count

**Usage**: `python scripts/update_docs_metrics.py`

### 2. Git Hooks ✅
**Files**:
- `.git/hooks/pre-commit` (installed)
- `scripts/git-hooks/pre-commit` (template)
- `scripts/install_git_hooks.sh` (installer)

**Purpose**: Warn when code changes without doc updates

**Behavior**:
- Detects code file changes
- Warns if no docs updated
- Doesn't block commits (just warns)

### 3. Weekly Audit Process ✅
**Files**:
- `docs/processes/weekly-documentation-audit.md`
- `docs/drift-log.md`

**Purpose**: Catch drift early through regular spot checks

**Process**:
1. Run metrics script (5 min)
2. Spot check recent changes (10 min)
3. Quick Serena verification (10 min)
4. Document findings (5 min)

**Frequency**: Every Monday, 15-30 minutes

---

## Testing Results

### Metrics Script Test
**Command**: `python scripts/update_docs_metrics.py`
**Output**: `docs/metrics.md` created ✅
**Metrics**:
- Tests: [X] total
- Lines: [X] Python lines
- ADRs: 42
- Plugins: 4

### Git Hook Test
**Action**: Modified service file without docs
**Result**: Warning displayed ✅
**Behavior**: Commit allowed with warning

### Audit Process Test
**Files**: Both documentation files created ✅
**Completeness**: 50+ lines each
**Clarity**: Process clearly documented

---

## Drift Prevention Strategy

### Three Layers of Defense

**Layer 1 - Automated (Continuous)**:
- Git hook warns on every commit
- Takes 0 developer time
- Catches issues immediately

**Layer 2 - Regular (Weekly)**:
- 15-30 minute audit
- Spot checks recent changes
- Updates metrics
- Logs drift

**Layer 3 - Comprehensive (Quarterly/As-Needed)**:
- Full PROOF-style audit
- Only when major drift detected
- Prevents big surprises

---

## Files Created

**New Files**:
- [x] scripts/update_docs_metrics.py (170 lines)
- [x] scripts/git-hooks/pre-commit (60 lines)
- [x] scripts/install_git_hooks.sh (15 lines)
- [x] docs/metrics.md (generated, 50+ lines)
- [x] docs/processes/weekly-documentation-audit.md (80 lines)
- [x] docs/drift-log.md (50 lines)
- [x] dev/2025/10/13/proof-9-documentation-sync-completion.md (this report)

**Total**: 7 new files, ~425 lines of automation

---

## Next Steps

### Immediate
- [x] Systems created
- [x] Initial metrics generated
- [ ] Commit all sync infrastructure

### First Week
- [ ] Monday: Run first weekly audit
- [ ] Update drift log
- [ ] Verify git hook working

### Ongoing
- [ ] Weekly audits every Monday
- [ ] Quarterly review of automation effectiveness
- [ ] Improve scripts based on usage

---

## Stage 2 Complete! 🎉

**PROOF-9 completes Stage 2 (Documentation)**:
- ✅ PROOF-0: Reconnaissance (90 min)
- ✅ PROOF-1: GREAT-1 Docs (80 min)
- ✅ PROOF-3: GREAT-3 Docs (24 min)
- ✅ PROOF-8: ADR Completion (60 min)
- ✅ PROOF-9: Doc Sync Process (XX min)

**Total Stage 2**: ~4 hours actual (vs 8-12 hours estimated)
**Efficiency**: 2-3x faster than predicted!

---

**Completion Time**: [timestamp]
**Status**: PROOF-9 Complete ✅
**Stage 2 Status**: COMPLETE ✅
```

---

## Commit Strategy

### Create Clean Commit

```bash
# Stage all sync infrastructure
git add scripts/update_docs_metrics.py
git add scripts/git-hooks/
git add scripts/install_git_hooks.sh
git add docs/metrics.md
git add docs/processes/weekly-documentation-audit.md
git add docs/drift-log.md
git add dev/2025/10/13/proof-9-*.md

# Install the git hook
bash scripts/install_git_hooks.sh

# Commit
git commit -m "feat(PROOF-9): Establish documentation sync infrastructure

Created three-layer system to prevent future documentation drift:

1. Automated Metrics Script (scripts/update_docs_metrics.py)
   - Auto-generates docs/metrics.md with current stats
   - Tracks tests, lines, ADRs, plugins
   - Run on-demand to update docs

2. Git Hooks (scripts/git-hooks/pre-commit)
   - Warns when code changes without doc updates
   - Doesn't block commits, just raises awareness
   - Installable via scripts/install_git_hooks.sh

3. Weekly Audit Process
   - 15-30 minute Monday check-in
   - Spot verification of recent changes
   - Drift tracking in docs/drift-log.md
   - Prevents accumulation of inaccuracies

Files created: 7 files, ~425 lines of automation
Purpose: Never need full PROOF epic again - catch drift early

Part of: CORE-CRAFT-PROOF epic, Stage 2 (Documentation)
Completes: Stage 2 - Documentation track ✅"

# Push
git push origin main
```

---

## Success Criteria

### All Systems Created ✅
- [ ] Metrics script functional
- [ ] Git hook installed and tested
- [ ] Audit process documented
- [ ] Drift log initialized

### Testing Complete ✅
- [ ] Metrics script runs successfully
- [ ] Git hook warns appropriately
- [ ] Documentation files complete

### Committed ✅
- [ ] All files staged
- [ ] Descriptive commit message
- [ ] Pushed to main
- [ ] Completion report created

### Stage 2 Complete ✅
- [ ] PROOF-0 through PROOF-9 all done
- [ ] Documentation accuracy: 99%+
- [ ] Sync processes established
- [ ] Ready for Stage 3 (Precision)

---

## Time Budget

**Based on Efficiency Pattern**:

**Original Estimate**: 2-3 hours

**Predicted Actual**: 20-40 minutes
- System 1 (Metrics): 10 min
- System 2 (Git Hooks): 8 min
- System 3 (Audit Process): 7 min
- Verification: 5 min
- Output: 5 min

**Target Completion**: 7:00-7:15 PM

---

## What NOT to Do

- ❌ Don't create just documentation without actual scripts
- ❌ Don't skip testing the systems
- ❌ Don't make systems overly complex
- ❌ Don't forget to install the git hook
- ❌ Don't decide any system is "optional" after compaction

## What TO Do

- ✅ Create ALL three systems (metrics, hooks, process)
- ✅ Test each system works
- ✅ Keep systems simple and maintainable
- ✅ Document usage clearly
- ✅ Make scripts executable
- ✅ Generate initial metrics

---

## Context

**PM**: "Yes, I'd like to finish Stage 2 as things are going quite smoothly with little demand on me!"

**Status**:
- PROOF-0: ✅ (90 min)
- PROOF-1: ✅ (80 min)
- PROOF-3: ✅ (24 min)
- PROOF-8: ✅ (60 min)
- PROOF-9: In progress

**What This Achieves**:
- Completes entire Stage 2 (Documentation)
- Prevents future PROOF work
- Makes doc accuracy self-maintaining
- Sets up for Stage 3 (Precision) tomorrow

**Victory**: Full stage complete in one day! 🏆

---

**PROOF-9 Start Time**: 6:32 PM
**Expected Completion**: 7:00-7:15 PM (20-40 minutes)
**Stage 2 Completion**: Tonight! 🎉

**LET'S ESTABLISH THE SYNC SYSTEMS AND FINISH STAGE 2! 🚀**

---

*"The best documentation is self-updating documentation."*
*- PROOF-9 Philosophy*
