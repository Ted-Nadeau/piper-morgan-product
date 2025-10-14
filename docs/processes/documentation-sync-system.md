# Documentation Sync System

**Established**: October 13, 2025 (PROOF-9)
**Purpose**: Prevent documentation drift through automated checks

---

## Three-Layer Defense System

### Layer 1: Pre-Commit Hooks (Immediate)
**Location**: `.git/hooks/pre-commit`
**Framework**: `pre-commit` (pre-commit.com)
**Frequency**: Every commit
**Action**: Runs configured quality checks before commit

**What it does**:
- Enforces code formatting (black, isort, flake8)
- Checks documentation quality
- Validates file structure
- Prevents common errors
- Configured via `.pre-commit-config.yaml`

**Installation**: `pre-commit install` (already installed)

---

### Layer 2: Weekly Audit (Regular)
**Location**: `.github/workflows/weekly-docs-audit.yml`
**Frequency**: Every Monday at 9:00 AM Pacific
**Action**: Creates GitHub issue with comprehensive checklist

**What it includes**:
1. **Claude Project Knowledge Updates** (Priority)
   - Lists all modified docs from past week
   - Identifies files needing project knowledge sync
   - Prevents Claude drift from documentation

2. **Automated Audits** (Claude Code /agent commands)
   - Stale content detection (>30 days)
   - Duplicate file identification
   - Broken link checking
   - Cross-reference verification

3. **Infrastructure Verification**
   - Port documentation (8001 not 8080)
   - Pattern compliance checks
   - Line count monitoring (web/app.py threshold: 1000 lines)
   - Mock fallback detection

4. **Session Log Management**
   - Completed session logs in `dev/YYYY/MM/DD/` structure
   - Omnibus synthesis identification
   - Cross-session pattern recognition

5. **Sprint & Roadmap Alignment**
   - Roadmap updates with completed items
   - GitHub issue taxonomy verification
   - Sprint goal tracking

6. **Pattern & Knowledge Capture**
   - Pattern catalog updates (33 patterns in 5 categories)
   - **CITATIONS.md completeness** (`docs/references/CITATIONS.md`)
   - Attribution verification (DDD, MCP, spatial intelligence, tooling)
   - Methodology improvements

7. **Quality Checks**
   - Methodology file organization
   - ADR numbering and location
   - Backup file detection
   - **Root README.md freshness** (repository view)
   - TODO/FIXME tracking

8. **Meta/Recursive Improvement**
   - Review sweep for process improvements
   - Incorporate PM feedback
   - Update workflow with improvements
   - Self-improving system

**Duration**: 15-30 minutes
**Owner**: PM or designated team member

---

### Layer 3: Automated Metrics (On-Demand)
**Location**: `scripts/update_docs_metrics.py`
**Output**: `docs/metrics.md`
**Frequency**: As needed (run before documentation updates)
**Action**: Generates current codebase statistics

**What it tracks**:
- **Test Coverage**:
  - Total test files: 260
  - Contract tests: 5
  - Regression tests: 2

- **Codebase Size**:
  - Services: 81,057 lines
  - Tests: 76,521 lines
  - Web: 1,075 lines
  - CLI: 3,033 lines

- **Architecture**: 42 ADRs
- **Plugins**: 4 operational (github, slack, notion, calendar)

**Usage**:
```bash
python scripts/update_docs_metrics.py
```

**When to run**:
- Before updating documentation with metrics
- During weekly audit
- Before major releases
- After significant code changes

---

## How They Work Together

### During Development (Layer 1):
1. Developer makes code changes
2. Attempts to commit
3. Pre-commit hooks run automatically
4. Formatting/quality checks enforce standards
5. Commit proceeds if checks pass

### Weekly Check-In (Layer 2):
1. Every Monday: GitHub Action runs
2. Creates issue #238 with comprehensive checklist
3. PM or team member reviews past week's changes
4. Identifies documentation drift
5. Updates Claude project knowledge
6. Catches anything missed during development

### Documentation Updates (Layer 3):
1. Developer needs to update documentation
2. Runs metrics script: `python scripts/update_docs_metrics.py`
3. Gets current, verified numbers
4. Updates documentation with accurate metrics
5. Commits `docs/metrics.md` with changes

---

## When to Do Full PROOF Work

**Weekly audits are lightweight checks (15-30 min).**

Escalate to full PROOF-style audit when:

- **Minor Drift** (<5% inaccuracy):
  - Note for next quarterly review
  - Track in weekly audit findings

- **Major Drift** (>10% inaccuracy):
  - Create PROOF-style epic (like PROOF-1, PROOF-3, PROOF-8)
  - Full documentation verification
  - Comprehensive corrections

- **Pattern of Drift**:
  - Improve automation scripts
  - Add checks to weekly audit
  - Update pre-commit hooks if needed

---

## System Maintenance

### Weekly (Automated)
- ✅ GitHub Action creates audit issue
- ✅ Team completes checklist (15-30 min)
- ✅ Drift tracked and addressed

### Monthly
- Review weekly audit findings for patterns
- Check if metrics script needs updates
- Verify pre-commit hooks still working
- Update CITATIONS.md if new tools/frameworks added

### Quarterly
- Full documentation accuracy audit
- Update automation scripts
- Improve checklists based on drift patterns
- Review and refine three-layer system

---

## Recent Updates

**October 13, 2025** (PROOF-9):
- ✅ Created automated metrics script
- ✅ Documented complete three-layer system
- ✅ Verified existing weekly audit (comprehensive)
- ✅ Verified pre-commit framework (standard)

**October 13, 2025** (Morning session):
- ✅ Fixed CITATIONS.md reference in workflow
- ✅ Added root README.md review
- ✅ Added meta/recursive improvement section
- ✅ Updated CLAUDE.md line counts

---

## Success Metrics

**Documentation Accuracy**: 99%+ (after PROOF-1, PROOF-3, PROOF-8)

**Drift Prevention**:
- Layer 1: Immediate quality enforcement (every commit)
- Layer 2: Weekly drift detection (15-30 min/week)
- Layer 3: On-demand metric verification (as needed)

**Time Investment**:
- Development: 0 min (automated pre-commit)
- Weekly: 15-30 min (audit checklist)
- Quarterly: 2-4 hours (full PROOF audit if needed)

**Result**: Documentation stays current without heavy ongoing investment.

---

## References

- **Weekly Audit Workflow**: `.github/workflows/weekly-docs-audit.yml`
- **Pre-Commit Config**: `.pre-commit-config.yaml`
- **Metrics Script**: `scripts/update_docs_metrics.py`
- **Current Metrics**: `docs/metrics.md` (auto-generated)
- **PROOF Epic Documentation**: `dev/2025/10/13/proof-*-completion.md`

---

*Part of CORE-CRAFT-PROOF (Stage 2: Documentation)*
*"The best documentation is self-updating documentation."*
