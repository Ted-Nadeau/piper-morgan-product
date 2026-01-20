# MUX Experience Tests Documentation

## Purpose

Verify that features can be described using experience language ("Piper noticed...") rather than database language ("Query returned...").

Experience tests are the canary in the coal mine - if we cannot describe a feature using the grammar, we've lost consciousness in the implementation.

## The Object Model Grammar

**"Entities experience Moments in Places."**

This sentence is the foundation. Every feature must be expressible using these three substrate protocols plus the supporting vocabulary:

- **Entities**: Actors with identity and agency
- **Moments**: Bounded significant occurrences with theatrical unities
- **Places**: Contexts with atmosphere where action happens

## Morning Standup (Reference Implementation)

### Grammar Expression

| Element | Value | Description |
|---------|-------|-------------|
| Entities | User, Piper | Actors with agency who experience the moment |
| Moment | Standup conversation | Bounded, significant occurrence with beginning/middle/end |
| Places | Calendar, GitHub | Contexts with atmosphere (meetings, code review) |
| Lenses | Temporal, Priority, Collaborative | Perceptual dimensions for viewing information |
| Situation | "Preparing for the day" | Frame with dramatic tension |

### Experience Language (PASS)

These expressions demonstrate consciousness-preserving language:

- "Piper noticed that you have 3 meetings today"
- "Piper remembers that you completed 2 PRs yesterday"
- "Piper anticipates a busy afternoon based on your calendar"
- "I sense a pattern in your Monday mornings"
- "This has caught my attention - it seems significant"

### Database Language (FAIL)

These expressions indicate flattening to data manipulation:

- "Query returned 3 calendar events"
- "Found 2 merged PRs in date range"
- "Calculated meeting density > threshold"
- "SELECT COUNT(*) FROM meetings WHERE date = today"
- "Row inserted into tasks table"

## Anti-Flattening Test Categories

### 1. Entity Tests (4 tests)
Verify that entities preserve identity, not just IDs.

**Pass criteria:**
- Entity has type describing role (user, assistant, team)
- Entity has name/identity beyond primary key
- Entity can have agency (can_initiate, can_respond)

**Fail indicators:**
- Entity is just `{ id: string }`
- No semantic information about WHO the entity is
- Entity cannot take action

### 2. Moment Tests (3 tests)
Verify that moments preserve significance, not just timestamps.

**Pass criteria:**
- Moment has description explaining what it IS
- Moment has significance explaining why it MATTERS
- Moment can capture outcomes and be remembered

**Fail indicators:**
- Moment is just `{ start_time, end_time }`
- No semantic information about the experience
- Moments are queryable but not memorable

### 3. Place Tests (3 tests)
Verify that places preserve atmosphere, not just configuration.

**Pass criteria:**
- Place has modality describing HOW interaction happens
- Place has atmosphere describing what it FEELS like
- Place has affordances describing what CAN happen there

**Fail indicators:**
- Place is just a connection string or endpoint URL
- No information about character or experience
- Places are interchangeable containers

### 4. Lifecycle Tests (5 tests)
Verify that lifecycle includes composting, not just deletion.

**Pass criteria:**
- COMPOSTED state exists as terminal state
- Composting extracts lessons and wisdom
- Each state has experience phrase explaining consciousness
- Lifecycle tells a story (narrative, not audit log)

**Fail indicators:**
- Objects are simply deleted
- No learning extracted from lifecycle journey
- States are just status codes (1, 2, 3...)

### 5. Metadata Tests (5 tests)
Verify that metadata captures knowledge ABOUT knowledge.

**Pass criteria:**
- Provenance tracks WHERE with confidence
- Freshness decays (knowledge ages)
- Journal separates facts (session) from meaning (insight)
- Confidence knows WHY it's confident

**Fail indicators:**
- Metadata is just attribute columns
- No distinction between facts and interpretation
- No temporal decay or aging

### 6. Ownership Tests (4 tests)
Verify that ownership describes relationships, not just foreign keys.

**Pass criteria:**
- Multiple ownership categories (NATIVE, FEDERATED, SYNTHETIC)
- Categories have consciousness metaphors (Mind, Senses, Understanding)
- Experience phrases use first person ("I know this because...")

**Fail indicators:**
- Ownership is just owner_id field
- No semantic categories for relationship types
- No explanation of how Piper relates to the object

### 7. Design Principle Tests (4 tests)
Verify that CXO design principles are honored.

**Pass criteria:**
- "I sense..." not "status=1"
- "transformed" not "deleted"
- Learning language in insights
- Resolver provides reasoning, not just results

**Fail indicators:**
- Database language exposed in interfaces
- Status codes instead of experience phrases
- Black-box operations without explanation

### 8. Grammar Integration Tests (3 tests)
Verify the complete grammar works together.

**Pass criteria:**
- Morning standup expressible without inventing new concepts
- Protocol methods use experience language (experiences, contains, captures)
- Grammar concepts are distinct from database concepts

**Fail indicators:**
- Need to invent new concepts for basic features
- Methods named get/set/update/delete
- Grammar concepts are just table name aliases

### 9. Consciousness Vocabulary Tests (3 tests)
Verify consciousness vocabulary throughout implementation.

**Pass criteria:**
- Ownership metaphors reference Mind/Senses/Understanding
- Lifecycle phrases use "I" or "This" (first-person perspective)
- Journal separates facts from meaning

**Fail indicators:**
- Third-person impersonal language everywhere
- No distinction between what happened and what it meant
- Machine-like language (process, execute, terminate)

### 10. Transition Tests (3 tests)
Verify state transitions preserve meaning.

**Pass criteria:**
- Invalid transitions explain what's wrong and valid options
- Transitions are forward-only (lifecycle is a journey)
- COMPOSTED is terminal by design (nothing beyond compost)

**Fail indicators:**
- Silent failures on invalid transitions
- Arbitrary state changes allowed
- Objects can be resurrected from COMPOSTED

### 11. Cathedral Test (3 tests)
The ultimate integration test - is this a cathedral or a shed?

**Pass criteria:**
- All core concepts have experience language
- The grammar is complete (3 protocols, 3 ownership, 8 lifecycle, 6 metadata)
- Nothing truly disappears - everything transforms

**Fail indicators:**
- Mechanical implementation without soul
- Incomplete grammar requiring workarounds
- Delete operations instead of composting

## Verification Checklist

For each major feature, verify:

1. [ ] CAN describe using "Piper noticed/remembers/anticipates..."
2. [ ] CANNOT accurately describe using "Query/Database/Record..."
3. [ ] Grammar elements (Entity/Moment/Place) are identifiable
4. [ ] Lenses can be applied for different perspectives
5. [ ] Situation frame captures dramatic tension
6. [ ] Lifecycle states make sense for the feature
7. [ ] Ownership category is clear (who created/observed/derived this?)
8. [ ] Metadata dimensions are applicable
9. [ ] Composting extracts wisdom if applicable

## Test Locations

| Test Suite | Location | Test Count |
|------------|----------|------------|
| Anti-Flattening | `tests/unit/services/mux/test_anti_flattening.py` | 40 |
| Protocols | `tests/unit/services/mux/test_protocols.py` | varies |
| Ownership | `tests/unit/services/mux/test_ownership.py` | 25 |
| Lifecycle | `tests/unit/services/mux/test_lifecycle.py` | 69 |
| Metadata | `tests/unit/services/mux/test_metadata.py` | 67 |
| Lenses | `tests/unit/services/mux/lenses/` | 101 |

## Running Experience Tests

```bash
# Run anti-flattening tests specifically
pytest tests/unit/services/mux/test_anti_flattening.py -v

# Run all MUX tests
pytest tests/unit/services/mux/ -v

# Check test count
pytest tests/unit/services/mux/ --collect-only -q | tail -3
```

---

*Part of MUX-399-PZ: Verification & Anti-Flattening Tests*
*Created: 2026-01-19*
