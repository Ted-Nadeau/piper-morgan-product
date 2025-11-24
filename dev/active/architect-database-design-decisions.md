# Database Design Decisions Package

**For**: Chief Architect
**From**: Research Code (Claude Code)
**Date**: 2025-11-19 16:45 PM PT
**Context**: Ted Nadeau architecture review follow-up questions

---

## Executive Summary

Ted Nadeau (brilliant computer scientist advisor) raised 6 database design questions that warrant strategic architectural decisions. This document summarizes current state, Ted's recommendations, research findings, and recommended paths forward.

**Key decisions needed**:
1. **Stored procedures**: Application-layer (Python) vs database-layer (PL/pgSQL)
2. **PK naming**: Unprefixed `id` vs prefixed `user_id`
3. **Keyspace partitioning**: Sequential IDs vs partitioned ranges vs UUIDs
4. **Table naming**: Plural (`users`) vs singular (`user`)
5. **Database annotations**: Ted's novel pattern for capturing WHY data changes
6. **Email integration**: How email-based workflows fit into architecture

**Immediate actions**:
- ✅ Document application-layer procedures pattern (Issue #331)
- ✅ Adopt Ted's annotation pattern (Issue #329) - **HIGH VALUE**
- 📝 Document naming conventions for new tables (Issues #339, #340)
- ⏳ Defer keyspace partitioning (UUIDs sufficient for alpha)

---

## 1. Stored Procedures: Application vs Database Layer

### Ted's Question
> "Are there stored procedures in use?"

### Current State

**NO** SQL stored procedures (PL/pgSQL) in PostgreSQL
**YES** application-layer "stored procedures" in Python:

- **Orchestration Engine** (`services/orchestration/engine.py`) - Multi-step workflows
- **Workflow Factory** (`services/workflows/`) - Parameterized workflow templates
- **Skills System** (`services/skills/`) - MCP-integrated capabilities
- **Intent Handlers** (`services/intent/intent_service.py`) - ~25 intent-to-action mappings

**Example application-layer procedure**:
```python
# services/orchestration/engine.py
async def execute_architecture_review_workflow(email: Email) -> WorkflowResult:
    """Multi-step procedure for architecture reviews"""
    questions = await self.parse_questions(email)
    research = await self.research_service.investigate(questions)
    draft = await self.drafting_service.create_reply(email, research)
    artifacts = await self.artifact_service.create(research)
    approval = await self.approval_service.request(draft)
    return WorkflowResult(draft=draft, artifacts=artifacts)
```

### Ted's Implicit Recommendation

Given he asked "are there stored procedures", likely checking if we're using database-layer procedures (standard practice for complex business logic).

### Research Code Recommendation

**Keep application-layer procedures** (Python workflows) for alpha/MVP.

**Rationale**:
- ✅ **Testability**: pytest > pgTAP (Python tests easier)
- ✅ **Version control**: Git tracks Python changes clearly
- ✅ **Type safety**: mypy validates workflows statically
- ✅ **AI comprehension**: LLMs read/modify Python >> PL/pgSQL
- ✅ **Debugging**: Python debugger >> PostgreSQL logs
- ✅ **Modularity**: Workflows compose services cleanly

**Trade-offs**:
- ❌ Network overhead (multiple DB round-trips)
- ❌ Can't leverage DB atomic transactions across all steps
- ❌ Potential performance issues for high-frequency operations

**When to reconsider** (add DB procedures):
- High-frequency operations need <10ms latency
- Complex SQL aggregations better expressed in database
- Cross-database transactions (multi-tenant sharding)

**Action**: Create ADR-013 documenting this pattern (Issue #331)

---

## 2. Primary Key Naming: Prefixed vs Unprefixed

### Ted's Question
> "Are the primary keys just 'id' or are they prefixed with table name e.g. user_id (probably preferred as less confusing)"

### Current State

**ALL tables use unprefixed `id`**:
```sql
lists.id           -- NOT lists.list_id
intents.id         -- NOT intents.intent_id
users.id           -- NOT users.user_id
```

**Foreign keys ARE prefixed**:
```sql
list_items.list_id → lists.id           ✅ FK prefixed
intents.workflow_id → workflows.id      ✅ FK prefixed
```

**Inconsistency**: FKs prefixed, PKs they reference are not.

### Ted's Recommendation

**Prefixed PKs** (`user_id` not `id`)

**Why prefixed is better**:
- Less confusing in JOINs (no ambiguous `id` columns)
- Self-documenting (`user_id` clearly from users table)
- Prevents debugging confusion ("ID 12345" → is that a user or conversation?)
- Consistent: PK and FK use same name

### Research Code Recommendation

**AGREE with Ted** - Prefixed PKs are clearer.

**Strategy**:
1. **NEW tables**: Use prefixed PKs going forward (`organization_id`, `session_id`)
2. **Existing tables**: Leave as-is for alpha/MVP (too risky to rename 27 tables)
3. **Post-MVP**: Decide if full migration worth it (40-60 hours effort, breaking change)

**Example for new tables**:
```sql
CREATE TABLE organization (
    organization_id UUID PRIMARY KEY,  -- Prefixed
    name VARCHAR(255),
    ...
);
```

**Migration risk**: Renaming existing PKs affects:
- All FK constraints (50+ to update)
- All SQLAlchemy models
- All queries in codebase
- All API responses

**Action**: Document convention in style guide (Issue #339)

---

## 3. Keyspace Partitioning: Sequential vs Partitioned vs UUIDs

### Ted's Question
> "Should the keyspace for each table be partitioned e.g. start at a different base number e.g. users start at 1m, conversations at 10m, etc."

### Current State

**UUID strategy** for most domain models:
```python
# services/domain/models.py
@dataclass
class KnowledgeNode:
    id: str = field(default_factory=lambda: str(uuid4()))  # UUID v4
```

**No keyspace partitioning** - UUIDs are random, globally unique.

### Ted's Suggestion

**Partitioned keyspaces**:
- Users: 1,000,000 - 1,999,999
- Conversations: 10,000,000 - 10,999,999
- Patterns: 20,000,000 - 20,999,999

**Benefits**:
- Sharding-ready (route queries by ID range)
- Debugging ("ID 10,234,567 = definitely a conversation")
- Capacity planning (know when approaching limits)

**Drawbacks**:
- Exposes table counts (security: "They have 50K users!")
- Complex sequence management
- Migration complexity (renumber existing records)

### Research Code Recommendation

**Defer keyspace partitioning** - UUIDs are better for alpha/MVP.

**Why UUIDs are better for Piper**:
- ✅ Globally unique (distributed systems ready)
- ✅ No sequence conflicts (multi-instance writes)
- ✅ Security (can't enumerate users by incrementing IDs)
- ✅ Client-side generation (reduce DB round-trips)

**When partitioned keyspaces make sense**:
- High-scale sharded databases (100M+ records/table)
- Manual shard routing by ID range
- Predictable ID exhaustion monitoring

**Alternative (future)**: **Snowflake IDs** if scaling demands it
- 64-bit integer with embedded timestamp + table type + sequence
- Sortable by creation time
- Table type in high bits (users = 1xxx, conversations = 2xxx)

**Action**: Document UUID strategy in ADR, defer partitioning until multi-tenant scaling

---

## 4. Table Naming: Singular vs Plural

### Ted's Question
> "suggest table names be singular 'user' not plural 'users' (annoying plural suffixes 'ies' in english)"

### Current State

**26 out of 27 tables use PLURAL naming**:
```sql
users          (not 'user')
lists          (not 'list')
intents        (not 'intent')
workflows      (not 'workflow')
conversations  (not 'conversation')
```

**Only singular**: `alembic_version` (Alembic's own table)

### Ted's Recommendation

**Singular table names** (`user` not `users`)

**Why singular is better**:
- Avoids plural edge cases (`category` → `categories`, `person` → `people`)
- Matches ORM model names (`User` model → `user` table, not `users`)
- Clearer foreign key semantics (`list.owner_id → user.id` reads better)
- Industry best practice (Microsoft, Oracle conventions)

### The Great Debate

**Arguments FOR Plural** (current state):
- Table IS a collection ("users" semantically correct)
- SQL reads naturally: `SELECT * FROM users`
- Rails/Django convention

**Arguments FOR Singular** (Ted's preference):
- No plural edge cases
- ORM alignment (singular model → singular table)
- Clearer FK reading

### Research Code Recommendation

**AGREE with Ted** - Singular is cleaner, ESPECIALLY for edge cases.

**Strategy**:
1. **NEW tables**: Use singular names (`organization`, `session`, `team`)
2. **Existing tables**: Leave plural for alpha/MVP (too risky to rename)
3. **Post-MVP**: Likely NOT worth migrating (60-80 hours, breaking change)

**Accept mixed convention**: Legacy plural, new singular (document in style guide)

**Action**: Document convention in style guide (Issue #340)

---

## 5. Database Annotations (Ted's Patented Innovation!)

### Ted's Question
> "Is there a way to 'annotate' the data in the database (much like code is annotated)? E.g., a configuration parameter was '10' but then was changed to '100' because of <reason> (by who, starting-when, why, etc.)? (this is one of my inventions that I've never seen anyone else do - patent-ted)"

### Current State

**Partial implementation** via `audit_logs` table:
```sql
CREATE TABLE audit_logs (
    old_value JSON,     -- ✅ Before value
    new_value JSON,     -- ✅ After value
    message TEXT,       -- ⚠️ Generic message
    details JSON,       -- ⚠️ Could hold annotation, but not standardized
    ...
);
```

**What's missing**:
- Structured annotation format (who, why, expected_outcome, actual_outcome)
- User-provided annotations (UI/API for "explain this change")
- AI-queryable rationale
- Learning from annotations

### Ted's Innovation: Annotating DATA (not just events)

**Example annotation**:
```sql
-- Hypothetical: Annotated config change
INSERT INTO data_annotations VALUES (
    'learning_settings',
    'pattern_threshold',
    'user_123',
    '{"threshold": 10}',   -- old_value
    '{"threshold": 100}',  -- new_value
    'Increased threshold from 10 to 100 because getting too many low-confidence pattern suggestions. User reported 80% false positive rate.',  -- ← Annotation!
    'Reduce FP rate to <20%',  -- expected_outcome
    '{"fp_rate_before": 0.80}', -- metrics
    'user_provided',
    '2025-11-19 15:30:00'
);

-- Later, after measuring impact:
UPDATE data_annotations
SET actual_outcome = 'FP rate dropped to 15% after change',
    related_metrics = '{"fp_rate_after": 0.15, "improvement": 0.65}'
WHERE annotation_id = '...';
```

### Why This is BRILLIANT for Piper

**Piper is an AI PM that learns from user behavior**. Annotating *why* configurations changed creates a **knowledge graph of tuning decisions**:

1. **LLM can query annotations**: "Why is threshold 100?" → Retrieve human explanation
2. **Pattern learning**: Identify which config changes improved outcomes
3. **Explain recommendations**: "I suggest increasing threshold to 150 because last time you increased from 10→100 it reduced FP by 65%"
4. **Audit trail for AI decisions**: When Piper auto-tunes, log WHY
5. **Institutional knowledge**: Capture PM's reasoning for future reference

### Research Code Recommendation

**IMPLEMENT Ted's annotation pattern immediately** - This is a **killer feature**.

**Novel contribution**: Traditional audit logs track WHAT changed (compliance/security). Ted's pattern tracks WHY (learning/reasoning/knowledge building). **This enables AI systems to learn from human expertise.**

**Implementation phases**:

**Phase 1 (MVP+1)**: Extend `audit_logs` table
```sql
ALTER TABLE audit_logs
    ADD COLUMN annotation TEXT,
    ADD COLUMN annotation_type VARCHAR(50),  -- 'user_provided', 'ai_generated', 'system'
    ADD COLUMN expected_outcome TEXT,
    ADD COLUMN actual_outcome TEXT,
    ADD COLUMN related_metrics JSONB;
```

**Phase 2 (Post-MVP)**: Dedicated `data_annotations` table
- Polymorphic annotations (any table, any column, any record)
- Link to knowledge graph nodes
- API endpoint for user annotations
- UI: "Annotate this change" button

**Phase 3 (Future)**: AI Learning Integration
- Query interface for similar changes
- Pattern detection in tuning decisions
- AI-suggested annotations based on context

**Research opportunity**: This could be a **research paper or patent**:
> "Annotated Databases: Capturing Rationale for Data Changes in AI-Augmented Systems"

**Prior art search needed**: Is anyone else doing this?

**Action**: Implement in 3 phases (Issue #329) - **PRIORITIZE THIS**

---

## 6. Email Integration Architecture

### Ted's Question
> "How do 'conversations' like this exist (or could exist) 'within' your infrastructure? ? AI can read mail? ? in-mail instead of out-mail"

### Current State

**3 input channels** (NOT email):
1. Web Chat (FastAPI WebSocket/HTTP)
2. Slack (webhooks, @piper mentions, channel listening)
3. CLI (terminal interaction)

**Current email workflow** (manual):
1. PM reads email (Gmail)
2. PM asks Claude Code to research + draft reply
3. Claude creates artifacts (drafts, issues, reports)
4. PM reviews, edits, sends manually

**What works well in Slack** (Ted convo could happen there):
```
PM: @piper Ted sent architecture questions. Research and draft reply.

[Piper spawns research agent, creates Beads]

Piper: ✅ Research complete!
- Reply draft: ted-nadeau-reply-draft.md (350 lines)
- GitHub issues: #319-#328
- QA report: qa-pre-mvp-technical-debt-report.md

Review and let me know if you want me to send or make changes.
```

### Research Code Recommendation

**Build email integration** in phases (Issue #330):

**Phase 1 (MVP+1)**: Read-only Gmail integration
- Gmail MCP adapter (OAuth, fetch emails, parse threads)
- Email intent classifier
- Slack notification when architecture review email arrives

**Phase 2 (MVP+1)**: Draft response workflow
- Orchestration engine executes "architecture review email" workflow
- Draft generated, sent to PM for approval via Slack
- PM reviews/edits/approves

**Phase 3 (MVP+2)**: Send email capability
- Send via Gmail API after approval
- Never auto-send (always requires human approval)
- AI authorship disclosure in signature

**Phase 4 (Future)**: Piper as email participant
- `piper@pipermorgan.com` email address
- Can be CC'd on threads
- Participates directly (with approval)

**Integration points**:
- Slack (approval workflow)
- Knowledge graph (link email discussions to decisions)
- Database annotations (Issue #329 - track email-based decisions)

**Action**: Build in phases (Issue #330) - Medium priority (Post-MVP)

---

## Strategic Recommendations Summary

| Decision | Ted's Preference | Current State | Recommendation | Priority |
|----------|------------------|---------------|----------------|----------|
| **Stored procedures** | N/A (checking if used) | Application-layer (Python) | Keep Python, document in ADR | Low (doc) |
| **PK naming** | Prefixed (`user_id`) | Unprefixed (`id`) | ✅ Adopt for NEW tables | Low (style) |
| **Keyspace partitioning** | Partitioned ranges | UUIDs | Defer - UUIDs sufficient | Low (future) |
| **Table naming** | Singular (`user`) | Plural (`users`) | ✅ Adopt for NEW tables | Low (style) |
| **Database annotations** | Annotate WHY changes | Partial (audit_logs) | ✅ **IMPLEMENT ASAP** | **HIGH** |
| **Email integration** | Enable email workflows | None | Build in phases (MVP+1) | Medium |

**Immediate high-value action**: **Database annotations (Issue #329)** - Novel feature, enables AI learning from human expertise.

**Quick wins**: Document PK/table naming conventions for new tables (Issues #339, #340)

**Defer**: Keyspace partitioning (UUIDs work great for alpha), full migration of existing tables (too risky)

---

## Open Questions for Chief Architect

1. **Database annotations**: Should we pursue patent/research paper for Ted's pattern?
2. **Naming conventions**: Accept mixed conventions (legacy plural, new singular) or bite the bullet and migrate?
3. **Email integration**: Is MVP+1 the right timing, or sooner?
4. **Stored procedures**: Any use cases where DB procedures make sense (analytics queries)?
5. **Scalability horizon**: When do we expect to need keyspace partitioning / Snowflake IDs?

---

## Related GitHub Issues

**Created from this research**:
- #329: Database annotation system (Ted's innovation) - **HIGH PRIORITY**
- #330: Email integration via Gmail MCP adapter
- #331: Document application-layer stored procedures (ADR)
- #336: Soft delete strategy (related to audit fields)
- #338: Migration rollback testing
- #339: Prefixed PK naming convention
- #340: Singular table naming convention

**Previously created**:
- #319-#328: Technical debt from initial architecture review

---

## Next Steps

**For Chief Architect**:
1. Review and approve database annotation pattern (Issue #329)
2. Decide on naming convention strategy (migrate existing or just new tables?)
3. Prioritize Issue #329 (annotations) for MVP+1
4. Discuss with Ted about patent/research paper opportunity

**For Development Team**:
1. Create ADR-013: Application-layer stored procedures (Issue #331)
2. Create ADR-014: Database annotation pattern (Issue #329)
3. Update style guide with PK/table naming conventions
4. Start Phase 1 of annotations (extend audit_logs)

**For Ted**:
1. Thank him for the annotation pattern idea (brilliant!)
2. Discuss prior art / patent opportunity
3. Invite to review annotation implementation design

---

**Prepared by**: Research Code (Claude Code)
**Date**: 2025-11-19 16:45 PM PT
**Session**: dev/active/2025-11-19-1259-research-code-log.md
**Total research time**: ~5 hours (across all sessions)
