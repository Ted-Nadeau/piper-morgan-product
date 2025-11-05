# Enhanced Pattern Sweep - Breakthrough Detection System

**Single Source of Truth** for running pattern analysis and breakthrough detection.

## Overview

The Enhanced Pattern Sweep is a multi-layer Pattern Intelligence System that automatically detects:
- **Methodology evolution** breakthroughs
- **Architectural insight** moments
- **Team coordination** patterns
- **Concept emergence** and growth
- **Meta-patterns** across project history

Unlike the original `pattern_sweep.py` (syntax-only), this system analyzes **the shape of work over time** to identify breakthrough moments with high confidence.

## Quick Start

### Analyze Recent Activity (Last 30 Days)
```bash
python scripts/pattern_sweep_enhanced.py
```

### Analyze Specific Date Range
```bash
python scripts/pattern_sweep_enhanced.py --start 2025-11-01 --end 2025-11-03
```

### Generate Detailed Report
```bash
python scripts/pattern_sweep_enhanced.py --verbose
```

### Export Results as JSON
```bash
python scripts/pattern_sweep_enhanced.py --format json --output results.json
```

### Run Single Analyzer
```bash
# Just temporal analysis (velocity, parallel work)
python scripts/pattern_sweep_enhanced.py --analyzer temporal

# Just semantic analysis (concept emergence)
python scripts/pattern_sweep_enhanced.py --analyzer semantic

# Just structural analysis (ADRs, refactoring)
python scripts/pattern_sweep_enhanced.py --analyzer structural
```

## Architecture

### Components

#### 1. TemporalAnalyzer (`temporal_analyzer.py`)
Analyzes **when and how fast** work happens:
- Commit velocity tracking (rolling windows)
- Velocity spike detection (>50% from baseline)
- Parallel session detection (concurrent agent work)
- Work intensity clustering
- Issue closure rate analysis

**Signals Emitted:**
- `VELOCITY_SPIKE` - Commit rate >50% above baseline
- `PARALLEL_WORK` - 3+ concurrent agents detected
- `COMPLETION_SPIKE` - Issue closure rate >2x average

#### 2. SemanticAnalyzer (`semantic_analyzer.py`)
Analyzes **what concepts emerge and evolve**:
- Term emergence tracking (68 key concepts)
- Growth rate calculation
- Context classification (ADR, omnibus, code, test, doc)
- Cross-validation scoring (multi-context appearances)
- Concept clustering (related terms)

**Signals Emitted:**
- `SEMANTIC_EMERGENCE` - 3+ new concepts appeared
- `ARCHITECTURAL_INSIGHT` - High-validation concepts (2+ contexts)

#### 3. StructuralAnalyzer (`structural_analyzer.py`)
Analyzes **architectural decisions and code structure**:
- ADR creation tracking (with git --follow)
- Refactoring event detection (>20 files changed)
- Class evolution tracking
- Import graph analysis
- Architectural pattern detection (Repository, Factory, Adapter, Service, Middleware)

**Signals Emitted:**
- `ADR_CREATION` - New ADR documented
- `REFACTORING_EVENT` - Major code restructuring (>30 files)

#### 4. BreakthroughDetector (`breakthrough_detector.py`)
**Synthesis engine** that combines signals to classify breakthroughs:

**Breakthrough Types:**
- **Implementation**: ADR creation + (refactoring | velocity spike)
- **Discovery**: Semantic emergence + (parallel work | architectural insight)
- **Coordination**: Parallel work + (velocity spike | completion spike)
- **Architectural**: Architectural insight + (ADR creation | refactoring)
- **Velocity**: Velocity spike + optional supporting signals
- **Completion**: Completion spike + optional supporting signals

**Confidence Scoring:**
- Base: Signal count / 4.0
- Bonus: +0.1 per supporting signal
- Convergence: +0.15 per additional analyzer involved
- Max: 1.0 (100%)

#### 5. PatternSweepEnhanced (`pattern_sweep_enhanced.py`)
CLI orchestrator with:
- Date range specification
- Output format selection (text/JSON)
- Single analyzer mode
- Verbose reporting
- File export

## Usage Patterns

### Weekly Sprint Review
```bash
# Analyze last sprint (7 days)
python scripts/pattern_sweep_enhanced.py --start $(date -d '7 days ago' +%Y-%m-%d) --verbose

# Export for PM review
python scripts/pattern_sweep_enhanced.py --start $(date -d '7 days ago' +%Y-%m-%d) \
    --format json --output "reports/sprint-$(date +%Y-%m-%d).json"
```

### Historical Analysis (All Omnibus Logs)
```bash
# Analyze entire project history (May 2025 - present)
python scripts/pattern_sweep_enhanced.py --start 2025-05-01 --end $(date +%Y-%m-%d) --verbose
```

### Validation Testing
```bash
# Test all analyzers
python scripts/test_temporal_analyzer.py
python scripts/test_semantic_analyzer.py
python scripts/test_structural_analyzer.py
python scripts/test_breakthrough_detector.py

# All tests should show ✅ PASSED
```

### Automated Monthly Report
```bash
# First of month - analyze previous month
python scripts/pattern_sweep_enhanced.py \
    --start $(date -d 'last month' +%Y-%m-01) \
    --end $(date -d 'last month' +%Y-%m-%d) \
    --format text \
    --output "reports/monthly-$(date -d 'last month' +%Y-%m).txt"
```

## Output Formats

### Text (Default)
Human-readable summary with:
- Breakthrough count and types
- Analysis metrics (velocity, concepts, ADRs, refactorings)
- Top breakthrough events with confidence scores

**Verbose mode** adds:
- Full signal list per breakthrough
- Analyzers involved
- Complete detection report

### JSON
Machine-readable format with:
- `breakthroughs[]` - All detected breakthrough events
- `signals{}` - All signals from all analyzers
- `signals_by_date{}` - Temporal clustering
- `analysis_metadata{}` - Per-analyzer statistics

Suitable for:
- Programmatic analysis
- Time-series visualization
- Integration with other tools
- Archival/historical tracking

## Key Concepts

### Signal Convergence
Multiple independent signals pointing to the same date = high confidence breakthrough. Example:
- Nov 1: `ADR_CREATION` + `REFACTORING_EVENT` + `PARALLEL_WORK` + `SEMANTIC_EMERGENCE`
- Result: Both IMPLEMENTATION and DISCOVERY breakthroughs detected (100% confidence)

### Cross-Context Validation
Concepts appearing in multiple contexts are more validated:
- **ADR + code + omnibus** = 100% validation (3/3 contexts)
- **Code + test** = 67% validation (2/3 contexts)
- **Code only** = 33% validation (1/3 contexts)

High-validation concepts trigger `ARCHITECTURAL_INSIGHT` signal.

### Temporal Clustering
Signals grouped by date reveal coordination patterns:
```
2025-11-01: [ADR_CREATION, REFACTORING_EVENT, PARALLEL_WORK, SEMANTIC_EMERGENCE]
2025-11-03: [PARALLEL_WORK, SEMANTIC_EMERGENCE, REFACTORING_EVENT]
```

Clustering shows Nov 1 had intense multi-dimensional activity, Nov 3 focused on discovery/coordination.

### Breakthrough Signatures
Different breakthrough types have distinct patterns:

**Implementation Breakthrough** (e.g., Nov 1):
- High ADR activity
- Major refactoring
- Documentation creation
- Code structure changes

**Discovery Breakthrough** (e.g., Nov 3):
- Concept emergence
- Parallel agent coordination
- Cross-validation
- Methodology insights

**Mixed Breakthroughs**: Same day can have multiple breakthrough types simultaneously!

## Validation

### Known Breakthroughs (Ground Truth)

**Nov 1, 2025**: Implementation Breakthrough
- ADR-040: "Local Database Per Environment"
- 4 refactoring events (2 architectural overhauls)
- 187 files changed in single commit
- ✅ Detected: 100% confidence

**Nov 3, 2025**: Discovery Breakthrough
- ActionHumanizer concept emergence
- 75% pattern concept emergence
- 5 parallel agent sessions
- EnhancedErrorMiddleware pattern
- ✅ Detected: 100% confidence

### Validation Tests
All tests pass with 75-100% detection rates:
```bash
$ python scripts/test_breakthrough_detector.py
🎯 Validation Score: 4/4 (100%)
✅ BreakthroughDetector validation PASSED
```

## Troubleshooting

### No Breakthroughs Detected
**Causes:**
- Date range too narrow (need wider window for baseline calculation)
- Low activity period (no significant patterns)
- Thresholds too strict

**Solutions:**
```bash
# Widen date range
python scripts/pattern_sweep_enhanced.py --start 2025-10-01 --end 2025-11-04

# Run verbose to see all signals
python scripts/pattern_sweep_enhanced.py --verbose

# Check individual analyzers
python scripts/pattern_sweep_enhanced.py --analyzer temporal
```

### Git History Issues
**Symptom:** ADRs not detected despite existing

**Cause:** Files moved/renamed (GitPython doesn't auto-follow)

**Solution:** Structural analyzer uses `git log --follow --diff-filter=A` to track true creation

### Session Log Parsing Failures
**Symptom:** No parallel work detected

**Cause:** Session log filename format mismatch

**Expected Format:** `YYYY-MM-DD-HHMM-role-agent-log.md`

**Solution:** Verify session logs follow naming convention:
```bash
ls dev/2025/11/03/
# Should show: 2025-11-03-0801-lead-sonnet-log.md
```

## Technical Details

### Git Commands Used
```bash
# ADR creation tracking
git log --follow --diff-filter=A --format="%ct %H" -- path/to/adr-040-*.md

# Commit velocity
git log --since="2025-11-01" --until="2025-11-04" --oneline

# File statistics
git diff --stat COMMIT_HASH
```

### Date Range Calculation
- Default: 30 days before end_date
- Baseline velocity: median of rolling 7-day windows
- Spike threshold: >50% above baseline

### Performance
- Full analysis (30 days): ~5-10 seconds
- Historical analysis (6 months): ~30-60 seconds
- Per-analyzer (30 days): ~2-3 seconds

## Integration Points

### GitHub Workflows
See `.github/workflows/pattern-sweep.yml` for automated monthly analysis.

### Omnibus Log Analysis
```bash
# Analyze specific omnibus period
python scripts/pattern_sweep_enhanced.py --start 2025-09-01 --end 2025-09-30
```

### CI/CD Integration
```yaml
# Add to .github/workflows/
- name: Run Pattern Sweep
  run: |
    python scripts/pattern_sweep_enhanced.py \
      --format json \
      --output pattern-sweep-results.json

- name: Upload Results
  uses: actions/upload-artifact@v3
  with:
    name: pattern-sweep
    path: pattern-sweep-results.json
```

## Files

### Production Code
- `pattern_analyzers/base.py` (217 lines) - Core data models
- `pattern_analyzers/temporal_analyzer.py` (435 lines) - Velocity tracking
- `pattern_analyzers/semantic_analyzer.py` (467 lines) - Concept emergence
- `pattern_analyzers/structural_analyzer.py` (412 lines) - ADR tracking
- `pattern_analyzers/breakthrough_detector.py` (407 lines) - Signal synthesis
- `pattern_sweep_enhanced.py` (284 lines) - CLI orchestrator

### Test Suite
- `test_temporal_analyzer.py` (154 lines)
- `test_semantic_analyzer.py` (187 lines)
- `test_structural_analyzer.py` (174 lines)
- `test_breakthrough_detector.py` (192 lines)

**Total**: 3,130 lines

## References

- **Original Pattern Sweep**: `scripts/pattern_sweep.py` (syntax-only analysis)
- **Enhancement Plan**: `dev/2025/11/02/pattern-sweep-enhancement-plan.md`
- **Implementation Log**: `dev/2025/11/04/2025-11-04-1002-prog-code-log.md`
- **Validation Data**: Nov 1-3, 2025 known breakthroughs

## Changelog

### v1.0.0 (2025-11-04)
- Initial implementation
- 3 analyzers (temporal, semantic, structural)
- Breakthrough synthesis engine
- CLI orchestrator with JSON export
- 100% validation against known breakthroughs

---

**Maintained by**: Piper Morgan Development Team
**Last Updated**: 2025-11-04
