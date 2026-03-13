# MUX Documentation Placement Audit

**Date**: 2026-01-20
**Purpose**: Review documentation created during MUX V1 sprint and verify proper placement per NAVIGATION.md

---

## Current MUX Documentation Inventory

### docs/internal/architecture/current/ (Architecture docs)

| File | Lines | Created | Purpose | Placement |
|------|-------|---------|---------|-----------|
| `consciousness-philosophy.md` | 966 | #400 | WHY - Philosophy foundation | ✅ Correct |
| `ownership-metaphors.md` | 1,449 | #405 | WHY - Ownership philosophy | ✅ Correct |
| `grammar-compliance-audit.md` | 787 | #404 | Audit of 16 features | ⚠️ Review |
| `feature-object-model-map.md` | 1,001 | #406 | Feature mappings | ⚠️ Review |

### docs/internal/architecture/current/patterns/ (Pattern catalog)

| File | Lines | Created | Purpose | Placement |
|------|-------|---------|---------|-----------|
| `pattern-050-context-dataclass-pair.md` | ~400 | #404 | Pattern | ✅ Correct |
| `pattern-051-parallel-place-gathering.md` | ~500 | #404 | Pattern | ✅ Correct |
| `pattern-052-personality-bridge.md` | ~450 | #404 | Pattern | ✅ Correct |
| `pattern-053-warmth-calibration.md` | ~480 | #404 | Pattern | ✅ Correct |
| `pattern-054-honest-failure.md` | ~450 | #404 | Pattern | ✅ Correct |
| `grammar-application-patterns.md` | 658 | #404 | Pattern index | ✅ Correct |

### docs/internal/development/ (Developer guides)

| File | Lines | Created | Purpose | Placement |
|------|-------|---------|---------|-----------|
| `grammar-onboarding-checklist.md` | 346 | #404 | Developer onboarding | ✅ Correct |
| `grammar-transformation-guide.md` | 1,171 | #404 | HOW to transform | ✅ Correct |
| `mux-experience-tests.md` | ~300 | #399 | Test criteria | ✅ Correct |
| `mux-implementation-guide.md` | ~350 | #399 | Implementation guide | ✅ Correct |

---

## Placement Analysis

### Per NAVIGATION.md Guidelines

**Architecture docs** (`internal/architecture/current/`):
- "Active architectural decisions"
- "Established patterns"
- ADRs and core specs

**Development docs** (`internal/development/`):
- "Working documents for active development"
- Tools, guides, methodologies

### Assessment

#### ✅ Correctly Placed

| Document | Location | Rationale |
|----------|----------|-----------|
| consciousness-philosophy.md | architecture/current | Core philosophy = architecture |
| ownership-metaphors.md | architecture/current | Core philosophy = architecture |
| pattern-050 through 054 | architecture/current/patterns | Patterns go in pattern catalog |
| grammar-application-patterns.md | architecture/current/patterns | Pattern index |
| grammar-transformation-guide.md | development | Developer how-to guide |
| grammar-onboarding-checklist.md | development | Developer onboarding |
| mux-implementation-guide.md | development | Implementation guidance |
| mux-experience-tests.md | development | Testing guidance |

#### ⚠️ Needs Review

| Document | Current Location | Question |
|----------|------------------|----------|
| grammar-compliance-audit.md | architecture/current | Is this an audit (temporary) or reference (permanent)? |
| feature-object-model-map.md | architecture/current | Is this reference architecture or planning? |

---

## Recommendation

### Option A: Keep Current Structure (Recommended)

**Rationale**: The current placement follows NAVIGATION.md principles:
- Philosophy docs → architecture/current (permanent reference)
- Patterns → architecture/current/patterns (established patterns)
- Guides → development (developer workflow)
- Audits/Maps → architecture/current (reference material for ongoing work)

The audit and feature map are **reference documentation** that developers will use when transforming features (#619-627), so architecture/current is appropriate.

### Option B: Create MUX Subdirectory

If MUX documentation grows significantly, consider:
```
docs/internal/architecture/current/mux/
├── philosophy/
│   ├── consciousness-philosophy.md
│   └── ownership-metaphors.md
├── reference/
│   ├── grammar-compliance-audit.md
│   └── feature-object-model-map.md
└── README.md (MUX architecture index)
```

**Not recommended yet** - current flat structure is navigable with 4 docs.

### Option C: Move Audit/Map to Planning

```
docs/internal/planning/current/mux/
├── grammar-compliance-audit.md
└── feature-object-model-map.md
```

**Not recommended** - these are reference docs, not planning docs.

---

## Navigation Updates Needed

Regardless of structure choice, NAVIGATION.md should be updated to include:

```markdown
### MUX Architecture Documentation

- **[Consciousness Philosophy](internal/architecture/current/consciousness-philosophy.md)** - WHY Piper has a soul
- **[Ownership Metaphors](internal/architecture/current/ownership-metaphors.md)** - Mind/Senses/Understanding philosophy
- **[Grammar Compliance Audit](internal/architecture/current/grammar-compliance-audit.md)** - Feature compliance assessment
- **[Feature Object Model Map](internal/architecture/current/feature-object-model-map.md)** - Feature-to-grammar mappings
- **[Grammar Application Patterns](internal/architecture/current/patterns/grammar-application-patterns.md)** - 5 patterns (050-054)

### MUX Developer Guides

- **[Grammar Transformation Guide](internal/development/grammar-transformation-guide.md)** - HOW to transform features
- **[Grammar Onboarding Checklist](internal/development/grammar-onboarding-checklist.md)** - Developer onboarding
- **[MUX Implementation Guide](internal/development/mux-implementation-guide.md)** - Technical implementation
- **[MUX Experience Tests](internal/development/mux-experience-tests.md)** - Consciousness test criteria
```

---

## Decision Required

**Question for PM**:
1. Keep current flat structure in architecture/current? (Recommended)
2. Create MUX subdirectory? (Future consideration if docs grow)
3. Update NAVIGATION.md with MUX section? (Yes, should do regardless)

---

*Audit complete: 2026-01-20*
