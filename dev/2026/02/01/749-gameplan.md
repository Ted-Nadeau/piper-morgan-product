# Gameplan: #749 - Knowledge Graph Entity Query Type Mismatch

**Issue**: #749
**Date**: 2026-02-01
**Type**: Bug Fix (Schema/Model Mismatch)
**Updated**: DDD-aligned approach per ADR-041

---

## Phase -1: Infrastructure Verification ✅

### Root Cause (Verified)

**Migration** `8e4f2a3b9c5d` line 78:
```python
sa.Column("node_type", sa.String(), nullable=False),  # VARCHAR - CORRECT per ADR-041
```

**Model** `services/database/models.py` line 776:
```python
node_type = Column(Enum(NodeType), nullable=False)  # WRONG - violates ADR-041
```

### ADR-041 Guidance

> "**ENUM vs String Types**: Use String in database (not PostgreSQL ENUMs)
> - Rationale: Flexible, no migrations for new values, matches migration intent"

The **migration is correct**. The **model violates ADR-041**.

### Decision: Align Model with ADR-041

- Database column stays as `VARCHAR` (correct)
- Model changes from `Enum(NodeType)` to `String` (fix)
- Conversion to Python enum happens in `to_domain()` (domain layer)

---

## Phase 0: Investigation ✅

### Files Affected

| File | Issue |
|------|-------|
| `services/database/models.py` | `KnowledgeNodeDB.node_type` uses `Enum()` |
| `services/database/models.py` | `KnowledgeEdgeDB.edge_type` likely same issue |

### Check for Similar Pattern

Need to verify `edge_type` column has same problem.

---

## Phase 1: Fix KnowledgeNodeDB

### Change 1: Column Type

```python
# Before (line 776):
node_type = Column(Enum(NodeType), nullable=False)

# After:
node_type = Column(String, nullable=False)
```

### Change 2: Verify to_domain() Conversion

```python
def to_domain(self) -> domain.KnowledgeNode:
    return domain.KnowledgeNode(
        id=self.id,
        name=self.name,
        node_type=NodeType(self.node_type),  # String → Enum
        # ...
    )
```

### Change 3: Verify from_domain() Conversion

```python
@classmethod
def from_domain(cls, node: domain.KnowledgeNode) -> "KnowledgeNodeDB":
    return cls(
        id=node.id,
        name=node.name,
        node_type=node.node_type.value,  # Enum → String
        # ...
    )
```

---

## Phase 2: Fix KnowledgeEdgeDB (if affected)

Same pattern for `edge_type` column if it uses `Enum(EdgeType)`.

---

## Phase 3: Verification

1. **Grep verification**: No `Enum(NodeType)` or `Enum(EdgeType)` in models
2. **Query test**: `get_nodes_by_type(NodeType.PERSON)` works
3. **Integration test**: Entity query succeeds during intent processing
4. **No errors**: Terminal shows no "Entity query failed" messages

---

## Acceptance Criteria

- [ ] `KnowledgeNodeDB.node_type` uses `String` column type
- [ ] `KnowledgeEdgeDB.edge_type` uses `String` column type (if applicable)
- [ ] `to_domain()` converts string to Python enum
- [ ] `from_domain()` converts Python enum to string
- [ ] No "operator does not exist: character varying = nodetype" errors
- [ ] Entity context enrichment succeeds

---

## STOP Conditions

- If existing data contains values not in NodeType enum → STOP
- If other models have same violation → expand scope, report to PM

---

## Evidence Required

- [ ] Model code showing `String` column type
- [ ] Grep showing no `Enum(NodeType)` usage
- [ ] Test showing query succeeds
- [ ] Terminal output without entity query errors
