# Gameplan: GREAT-1C Verification Phase

**Date**: September 25, 2025
**Issue**: GREAT-1C (#187) - Final Verification
**Architect**: Claude Opus 4.1
**Lead Developer**: [Newly onboarded]

---

## Mission: Verify Everything Works for Real Developers

### Remaining Checkboxes
1. ☐ Fresh clone and setup works without issues
2. ☐ New developer can understand orchestration flow
3. ☐ All tests pass in CI/CD pipeline
4. ✅ No remaining TODO comments without issue numbers (43% compliant, systematic tracking)
5. ☐ Performance benchmarks documented

One checkbox already validated (TODOs), four to verify.

---

## Infrastructure Verification Checkpoint

### What We Know Works
- QueryRouter: Operational (0.1ms access, 4500ms full pipeline)
- CI/CD: Performance and coverage enforcement active
- Documentation: Guides created
- Tests: 63 test files operational

### PM Verification Before Starting
```bash
# Verify CI is actually running
gh run list --limit 5

# Check if setup documentation exists
ls -la docs/guides/orchestration-setup-guide.md
ls -la docs/architecture/initialization-sequence.md

# Verify performance benchmarks location
find docs/ -name "*performance*" -o -name "*benchmark*" | grep -v node_modules
```

---

## Phase 1: Fresh Clone Verification (45 min)

### Deploy: Both Agents in Clean Environment

#### 1A. Prepare Clean Environment

**Code Instructions - Create Fresh Space**:
```markdown
Create a completely fresh environment:

1. In a new directory outside the project:
   ```bash
   cd /tmp
   mkdir fresh-clone-test
   cd fresh-clone-test
   ```

2. Clone the repository fresh:
   ```bash
   git clone https://github.com/mediajunkie/piper-morgan-product.git
   cd piper-morgan-product
   ```

3. Document initial state:
   - No virtual environment
   - No dependencies installed
   - No configuration files
```

**Cursor Instructions - Setup Following Docs**:
```markdown
Follow ONLY the setup documentation:

1. Use docs/guides/orchestration-setup-guide.md
2. Document every step followed
3. Note any missing instructions
4. Track time to operational state

Do NOT use prior knowledge - only what's documented.
```

#### 1B. Execute Setup Process

```bash
# Follow the documented setup exactly
# Expected steps (verify against actual docs):

# 1. Python environment
python3 -m venv venv
source venv/bin/activate

# 2. Dependencies
pip install -r requirements.txt

# 3. Configuration
cp config/example.env .env
# Edit .env per documentation

# 4. Database setup
python scripts/setup_database.py  # if documented

# 5. Verify operational
python main.py  # Should start without errors
```

#### 1C. Test Core Functionality

```bash
# Verify QueryRouter works
curl -X POST http://localhost:8001/api/intent \
    -H "Content-Type: application/json" \
    -d '{"message": "Create a GitHub issue"}'

# Run core tests
pytest tests/unit/test_queryrouter.py -v
```

### Evidence Collection
- Terminal output of entire setup process
- Time from clone to operational
- Any errors encountered
- Missing documentation gaps

---

## Phase 2: Developer Understanding Verification (30 min)

### Both Agents - Simulate New Developer Experience

#### 2A. Documentation Navigation Test

```markdown
Starting from docs/README.md, can a developer find:

1. Architecture overview? (Time to find: ___)
2. QueryRouter's role? (Time to find: ___)
3. How to add new intents? (Time to find: ___)
4. Troubleshooting guide? (Time to find: ___)
5. Performance expectations? (Time to find: ___)

Document the path taken to find each item.
```

#### 2B. Code Navigation Test

```markdown
Using only documentation, can a developer:

1. Locate QueryRouter implementation:
   - Where is the main class?
   - How does it connect to OrchestrationEngine?

2. Understand the flow:
   - Request entry point
   - Intent classification
   - Query routing
   - Response generation

3. Modify the system:
   - Where to add a new route?
   - How to test changes?
```

### Evidence Collection
- Documentation paths followed
- Time to understanding
- Clarity assessment (1-5 scale)
- Missing information list

---

## Phase 3: CI/CD Pipeline Verification (30 min)

### Deploy: Code for CI Analysis, Cursor for Manual Testing

#### 3A. Verify Current CI Status

**Code Instructions**:
```bash
# Check recent CI runs
gh run list --workflow=ci.yml --limit=10

# Get detailed status of latest run
gh run view [latest-run-id]

# Check specific job outputs
gh run view [run-id] --log

# Look for:
# - Test execution
# - Performance checks
# - Coverage enforcement
# - QueryRouter-specific tests
```

#### 3B. Trigger Fresh CI Run

**Cursor Instructions**:
```bash
# Create a small change to trigger CI
git checkout -b verification/ci-test
echo "# CI Verification $(date)" >> README.md
git add README.md
git commit -m "chore: CI verification test"
git push origin verification/ci-test

# Create PR to trigger full CI
gh pr create --title "CI Verification" --body "Testing CI pipeline"

# Monitor CI execution
gh pr checks
```

#### 3C. Verify All Tests Pass

Expected CI stages:
1. Setup environment ✓
2. Install dependencies ✓
3. Run unit tests ✓
4. Run integration tests ✓
5. Performance checks (< 5400ms) ✓
6. Coverage checks (tiered) ✓
7. QueryRouter lock tests ✓

### Evidence Collection
- CI run link
- All stages passing
- Performance metrics from CI
- Coverage reports from CI

---

## Phase 4: Performance Documentation (30 min)

### Both Agents - Locate and Verify Benchmarks

#### 4A. Find Performance Documentation

```bash
# Search for performance benchmarks
find docs/ -type f -exec grep -l "performance\|benchmark\|ms\|millisecond\|second" {} \;

# Expected locations:
# - docs/testing/performance-enforcement.md
# - docs/architecture/performance-benchmarks.md
# - README section on performance
```

#### 4B. Verify Benchmarks Are Current

```markdown
Performance benchmarks should document:

1. QueryRouter initialization: ~0.1ms
2. Intent classification: ~200ms (mocked) / ~2000ms (real LLM)
3. Full orchestration flow: ~4500ms
4. Acceptable degradation: 20% (5400ms threshold)

Verify these are documented and match reality.
```

#### 4C. Run Performance Tests for Comparison

```bash
# Run performance tests to verify documented benchmarks
PYTHONPATH=. python -m pytest tests/performance/ -v --tb=short

# Compare actual results to documentation
# Document any discrepancies
```

### Evidence Collection
- Location of performance documentation
- Documented benchmarks
- Actual test results
- Match/mismatch analysis

---

## Phase Z: Final Verification & Handoff

### Compile Evidence Package

1. **Fresh Clone Evidence**
   - Setup process output
   - Time to operational
   - Success/failure points

2. **Developer Understanding Evidence**
   - Documentation navigation results
   - Code understanding assessment
   - Missing information list

3. **CI/CD Evidence**
   - CI run links
   - All tests passing
   - Performance and coverage met

4. **Performance Documentation Evidence**
   - Documentation locations
   - Benchmark accuracy
   - Current test results

### GitHub Update

```markdown
## Verification Phase Complete

✅ Fresh clone and setup works without issues
- Setup time: X minutes
- Documentation followed successfully
- QueryRouter operational after fresh setup

✅ New developer can understand orchestration flow
- Architecture documented clearly
- QueryRouter role explained
- Modification points identified

✅ All tests pass in CI/CD pipeline
- CI run: [link]
- All stages passing
- Performance and coverage gates working

✅ No remaining TODO comments without issue numbers
- 43% compliant (43/101)
- Systematic tracking for remaining 58

✅ Performance benchmarks documented
- Located in: [paths]
- Current benchmarks accurate
- Thresholds realistic and enforced
```

---

## Success Criteria

- [ ] Fresh clone reaches operational state following only docs
- [ ] Developer can understand system in <30 minutes
- [ ] CI/CD shows all green
- [ ] Performance benchmarks documented and accurate
- [ ] All evidence collected and linked

---

## Time Estimate

- Phase 1: 45 minutes (fresh clone)
- Phase 2: 30 minutes (developer understanding)
- Phase 3: 30 minutes (CI/CD verification)
- Phase 4: 30 minutes (performance documentation)
- Phase Z: 15 minutes (evidence compilation)
- **Total: ~2.5 hours**

---

## STOP Conditions

- If fresh clone cannot reach operational state
- If documentation has major gaps
- If CI is not actually running tests
- If performance benchmarks don't exist

---

*Final verification for systematic completion - evidence over assumption.*
