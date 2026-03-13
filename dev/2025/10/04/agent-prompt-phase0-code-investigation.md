# Claude Code Agent Prompt: GREAT-3C Phase 0 - Investigation

## Session Log Management
Create new session log: `dev/2025/10/04/2025-10-04-phase0-code-investigation.md`

Update with timestamped entries for your work.

## Mission
**Investigate Developer Guide Requirements**: Determine what developers need to add new integrations, what patterns to document, and what makes a good template plugin.

## Context

**GREAT-3C Goal**: Document wrapper/adapter pattern and create developer resources.

**Current State** (from Phase -1):
- 4 plugins exist as thin wrappers (96-111 lines each)
- Routers contain business logic
- 48/48 tests passing
- No pattern documentation exists yet
- services/plugins/README.md exists (8.8KB)

## Your Tasks

### Task 1: Analyze Existing Plugin Structure

**Pick one plugin to study in detail** (suggest Slack as most complete):

```bash
# View complete plugin structure
ls -la services/integrations/slack/

# Read the plugin wrapper
cat services/integrations/slack/slack_plugin.py

# Read the router
head -50 services/integrations/slack/slack_integration_router.py

# Check config service
cat services/integrations/slack/config_service.py
```

**Questions to Answer**:
1. What does the plugin wrapper actually do? (What are its responsibilities?)
2. What does the router do? (Where is business logic?)
3. How do they interact?
4. What's the dependency flow? (Router → Plugin or Plugin → Router?)
5. Why is this a good pattern? (What does separation provide?)

### Task 2: Examine services/plugins/README.md

```bash
cat services/plugins/README.md
```

**Questions to Answer**:
1. What's already documented?
2. What's missing that developers would need?
3. Does it explain the wrapper pattern?
4. Does it show how to create a new integration?
5. What sections should a developer guide have?

### Task 3: Identify Template Plugin Requirements

**What would a template/example plugin need?**

Think about a developer who wants to add a new integration (e.g., "weather API"). What files would they need?

**Required Files**:
- `__init__.py` - What should be in it?
- `example_integration_router.py` - What's the minimum viable router?
- `example_plugin.py` - What's the minimum viable plugin wrapper?
- `config_service.py` - Standard config pattern?
- `test_example_plugin.py` - What tests are essential?

**Design Questions**:
1. Should example be functional (real API) or stub/mock?
2. What's the simplest useful example?
3. What patterns should it demonstrate?
4. Should it be copy-pasteable?

### Task 4: Review Current Documentation Strategy

```bash
# Check docs structure
ls -la docs/

# Check for architecture docs
ls -la docs/internal/architecture/

# See what's in STRUCTURE_PLAN
grep -A 10 "developer guide" docs/STRUCTURE_PLAN.md
```

**Questions to Answer**:
1. Where should plugin pattern docs live?
2. Where should developer guide live?
3. What's the existing documentation organization?
4. How do these fit into current structure?

### Task 5: Metadata Enhancement Planning

**Current plugin metadata** (from GREAT-3A/3B):
```python
class PluginMetadata:
    name: str
    version: str  # Currently blank or minimal
    description: str
    author: str
    capabilities: List[str]
    # ... what else?
```

**Questions**:
1. What version format? (semver? 1.0.0?)
2. Should all plugins start at 1.0.0?
3. What other metadata might be useful?
4. How to display versions to users?

### Task 6: Create Implementation Recommendations

Based on investigation, recommend:

**For Pattern Documentation** (Phase 1):
- File location and name
- Key sections to include
- Diagrams needed
- Examples to show

**For Developer Guide** (Phase 2):
- File location and name
- Table of contents
- Step-by-step flow
- Common patterns section

**For Template Plugin** (Phase 3):
- Example name (weather? demo? example?)
- Minimal functionality needed
- What to include in each file
- Testing approach

**For Metadata Enhancement** (Phase 4):
- Version format
- What to add to each existing plugin
- How to validate

## Deliverable

Create: `dev/2025/10/04/phase-0-code-investigation.md`

Include:
1. **Plugin Pattern Analysis**: How wrapper pattern works
2. **Current Documentation Review**: What exists, what's missing
3. **Template Requirements**: What a good example needs
4. **Documentation Strategy**: Where docs should live
5. **Metadata Plan**: Version format and additions
6. **Implementation Recommendations**: Clear guidance for Phases 1-4

## Success Criteria
- [ ] Wrapper pattern clearly understood
- [ ] Documentation gaps identified
- [ ] Template plugin requirements defined
- [ ] Metadata enhancement plan clear
- [ ] Implementation recommendations specific

## Notes
- Focus on what developers actually need
- Keep recommendations practical and copy-pasteable
- Consider maintenance burden of examples
- Think about "future you" reading these docs

---

**Deploy at 12:25 PM**
**Coordinate with Cursor on documentation organization**
