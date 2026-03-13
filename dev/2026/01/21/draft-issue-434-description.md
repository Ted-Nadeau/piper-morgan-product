# Draft Issue Description: #434 MUX-TECH-PHASE2-ENTITY

**Status**: ~30% complete (overlap analysis from V1)
**Estimated Remaining**: ~16h (revised from 24h original)

---

## Context Update (Jan 21, 2026)

This issue was written in December 2025 BEFORE the V1 sprint implementation (#399). The V1 sprint implemented significant foundation:

### What Already Exists (from #399)

| Spec Requirement | Status | Evidence |
|------------------|--------|----------|
| EntityProtocol | ✅ EXISTS | `services/mux/protocols.py:25` |
| Entity experiences Moment | ✅ EXISTS | `protocols.py:42` - `experiences()` method |
| Perception result | ✅ EXISTS | `services/mux/perception.py` - full implementation |
| PerceptionMode (temporal) | ✅ EXISTS | NOTICING, REMEMBERING, ANTICIPATING |
| "I notice" patterns | ✅ EXISTS | All 8 lenses use consciousness-preserving language |
| Consciousness terminology | ✅ EXISTS | Throughout lenses, lifecycle, protocols |

### What's Missing (X1 remaining work)

| Spec Requirement | Status | Gap Description |
|------------------|--------|-----------------|
| PiperEntity class | ❌ MISSING | No dedicated model for Piper-as-entity |
| AwarenessLevel enum | ❌ MISSING | sleeping/drowsy/alert/focused/overwhelmed |
| EmotionalState enum | ❌ MISSING | curious/concerned/satisfied/puzzled |
| ConsciousnessAttributes | ❌ MISSING | wants/fears/capabilities for entities |
| EntityRole enum | ❌ MISSING | ACTOR/PLACE/OBSERVER/PARTICIPANT |
| EntityContext tracking | ❌ MISSING | Track role in current moment |
| Five orientation queries | ❌ MISSING | Who/When/Where/What can/What should |
| ConsciousnessExpression | ⚠️ PARTIAL | Patterns exist in lenses, not as formal class |
| Add consciousness to User/Stakeholder | ❌ MISSING | consciousness: Optional[ConsciousnessAttributes] |

---

## Revised Scope

### Phase 1: Core Consciousness Enums (2h)
Create foundation enums in `services/mux/consciousness.py`:
- AwarenessLevel enum (5 states)
- EmotionalState enum (4 states)
- EntityRole enum (4 roles)

### Phase 2: ConsciousnessAttributes Dataclass (3h)
Create `ConsciousnessAttributes` for any entity:
- wants: List[str]
- fears: List[str]
- capabilities: List[str]
- knows_about: List[str]
- attention_on: Optional[str]
- emotional_state: Optional[str]
- trusts: Dict[str, float]
- depends_on: List[str]
- influences: List[str]

### Phase 3: PiperEntity Model (4h)
Create `PiperEntity` as first-class model:
- Identity (id, name, role, version)
- Consciousness state (awareness, attention, emotion)
- Agency (available/active/blocked capabilities)
- Boundaries (trust, ethical, knowledge)
- Five orientation queries
- Relationships (primary_user, known_entities, active_situations)

### Phase 4: EntityContext System (3h)
Create `EntityContext` for role tracking:
- entity_id
- current_role: EntityRole
- in_moment: Optional[str]
- in_place: Optional[str]
- as_entity/as_place booleans

### Phase 5: ConsciousnessExpression Class (2h)
Formalize existing patterns into a class:
- FIRST_PERSON_PATTERNS constant
- express_awareness() method
- Generate from consciousness state

### Phase 6: Domain Model Integration (2h)
Add `consciousness: Optional[ConsciousnessAttributes]` to:
- User
- Stakeholder
- Agent (if exists)
- Team (if exists)

---

## Acceptance Criteria (Updated)

- [ ] AwarenessLevel, EmotionalState, EntityRole enums exist
- [ ] ConsciousnessAttributes dataclass exists with all fields
- [ ] PiperEntity model exists with identity, consciousness, agency, boundaries
- [ ] Five orientation queries have model support
- [ ] EntityContext tracks entity's current grammatical role
- [ ] ConsciousnessExpression class generates first-person expressions
- [ ] Domain models (User, Stakeholder) can have consciousness attributes
- [ ] All existing MUX tests still pass (314)
- [ ] New unit tests for all new models (~30 tests)
- [ ] Morning Standup can theoretically use PiperEntity

---

## Verification

### Consciousness Test
Can Piper express: "I'm concerned that the sprint seems overloaded"?
- PiperEntity with emotional_state = CONCERNED
- attention_focus = ["sprint_planning"]
- ConsciousnessExpression.express_awareness() generates output

### Anti-Flattening Test
- Does Piper have identity or just functions? (Must have identity)
- Do entities have wants/fears or just properties? (Must have drives)
- Can entities play multiple roles? (Must support spectrum)

---

## Estimated Effort

| Phase | Hours |
|-------|-------|
| P1: Core enums | 2h |
| P2: ConsciousnessAttributes | 3h |
| P3: PiperEntity | 4h |
| P4: EntityContext | 3h |
| P5: ConsciousnessExpression | 2h |
| P6: Domain integration | 2h |
| **Total** | **16h** |

---

*Updated: 2026-01-21 - Lead Developer (Claude Code Opus)*
