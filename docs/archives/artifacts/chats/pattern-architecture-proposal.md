# Proposed Pattern Documentation Architecture
## September 15, 2025

### Current State (Fragmented)
```
docs/
├── development/
│   ├── methodology-core/        # Process patterns
│   └── pattern-catalog.md       # 2,703 line monolith
├── piper-education/
│   ├── decision-patterns/       # Teaching Piper decisions
│   ├── methodologies/           # Teaching Piper methods
│   └── implementation-guides/   # How-to patterns
└── analysis/                    # Various pattern discoveries

rag/pattern-sweeps/              # Automated + RAG analyses
```

### Proposed Structure (Unified)

```
patterns/                         # NEW: Single source of truth
├── README.md                     # Pattern taxonomy & navigation
├── discovered/                   # Patterns we've found
│   ├── code/
│   │   ├── async-patterns.md
│   │   ├── ddd-patterns.md
│   │   └── test-patterns.md
│   ├── methodology/
│   │   ├── excellence-flywheel.md
│   │   ├── verification-first.md
│   │   └── cascade-protocol.md
│   └── coordination/
│       ├── agent-handoff.md
│       └── binocular-analysis.md
├── applied/                      # Patterns in use
│   ├── current/                 # What we're using now
│   └── experimental/            # What we're trying
├── teaching/                     # For Piper education
│   ├── fundamental/             # Must-know patterns
│   └── advanced/                # Complex patterns
└── analysis/                     # Pattern sweep outputs
    └── 2025-09-15/              # Today's discoveries
```

### Pattern Lifecycle

1. **Discovery** → pattern sweep or human insight
2. **Documentation** → captured in discovered/
3. **Validation** → tested and refined
4. **Application** → moved to applied/current/
5. **Teaching** → distilled for Piper in teaching/

### Pattern Metadata Template

```markdown
# Pattern: [Name]

## Classification
- **Category**: code|methodology|coordination
- **Maturity**: emerging|validated|established
- **Source**: automated|discovered|inherited
- **First Seen**: YYYY-MM-DD
- **Confidence**: 0.0-1.0

## Description
What this pattern does and why it matters

## Examples
Concrete instances where we've seen this

## Application
How to use this pattern

## Related Patterns
Links to other patterns

## Evolution
How this pattern has changed over time
```

### Migration Plan

1. **Phase 1**: Create patterns/ structure
2. **Phase 2**: Extract patterns from:
   - pattern-catalog.md → individual files
   - methodology-core → patterns/discovered/methodology/
   - piper-education → patterns/teaching/
3. **Phase 3**: Integrate pattern sweep outputs
4. **Phase 4**: Deprecate old locations

### Benefits

- **Single source of truth** for all patterns
- **Clear lifecycle** from discovery to teaching
- **Metadata** for tracking pattern evolution
- **Separation** of human vs automated discoveries
- **Integration point** for pattern sweep outputs

### Pattern Attribution Model (from earlier discussion)

Patterns would be classified by their origin:
1. **Unique/idiosyncratic** - Piper Morgan special patterns
2. **Savvy tips** - Power user patterns
3. **AI-dev wisdom** - Patterns for AI-assisted development
4. **General practice** - Universal engineering principles

This helps distinguish what's transferable vs. personal preference.
