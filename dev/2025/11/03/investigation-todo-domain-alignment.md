# Investigation Mission: Todo Domain Model Alignment

**Priority**: CRITICAL - Architectural Foundation Check
**Time**: 30-45 minutes using Serena MCP
**Context**: Before implementing TodoManagementService, we need to verify our domain model

---

## Background: The Original Domain Vision

The PM's original design principle:
> **Lists and Items are cognitive primitives. Todo lists and tasks are just ONE type of list/item.**

This enables:
- Todo lists (with completion, priority)
- Shopping lists (with quantity, categories)
- Project backlogs (with story points)
- Reading lists (with progress tracking)
- Any future list type

**The Question**: Does our current todo implementation honor this vision, or have we built a todo-specific silo?

---

## Your Investigation Mission

Using Serena MCP for token-efficient code exploration, investigate and report on:

### 1. Find the Generic Foundation

```bash
# Use Serena to explore the generic list system
serena find_symbol UniversalListRepository
serena find_symbol UniversalList
serena find_symbol Item
serena find_symbol BaseList
```

Questions to answer:
- Does UniversalListRepository implement generic List and Item concepts?
- What are the primitive domain models?
- Is there a base Item class that todos could/should extend?

### 2. Analyze Todo Implementation

```bash
# Examine todo domain models
serena find_symbol Todo --type class
serena find_symbol TodoList --type class
serena analyze_relationship Todo Item
serena analyze_relationship TodoList List
```

Questions to answer:
- Does Todo extend a generic Item?
- Does TodoList extend a generic List?
- Or are they completely separate hierarchies?

### 3. Repository Relationship

```bash
# Compare the repositories
serena find_referencing_symbols UniversalListRepository
serena find_referencing_symbols TodoRepository
```

Questions to answer:
- Is TodoRepository a specialization of UniversalListRepository?
- Or are they parallel, unrelated systems?
- Could todos be stored as Items with type="todo"?

### 4. Check for Design Decisions

```bash
# Look for documentation of the design
grep -r "UniversalList" docs/ --include="*.md"
grep -r "domain.*model.*list" . --include="*.md"
find . -name "*ADR*" -type f | xargs grep -l "list\|todo"
```

Questions to answer:
- Is there an ADR explaining the lists/todos relationship?
- Any documentation of why the current design exists?
- Comments in code explaining the domain model?

### 5. Compatibility Analysis

Look at `services/repositories/todo_repository.py` line 1:
> "Manages Todo and TodoList entities with compatibility for universal lists"

Investigate:
- What does "compatibility for universal lists" mean?
- Is there a migration path between systems?
- Can todos work with both systems?

---

## Required Output

After investigation, provide:

### A. Current State Assessment

Choose one:
1. **✅ ALIGNED**: Todos properly extend generic lists/items as intended
2. **⚠️ DIVERGED**: Parallel todo system ignoring the generic foundation
3. **🔄 HYBRID**: Partial integration with both systems coexisting

### B. Evidence

Provide specific code examples:
```python
# Example: If aligned, show the inheritance
class Item:  # Generic primitive
    id: int
    text: str

class Todo(Item):  # Proper specialization
    completed: bool
    priority: str
```

Or if diverged:
```python
class Todo:  # Completely separate
    id: int
    title: str
    # No relationship to Item
```

### C. Recommendation

Based on findings, recommend:

**Option 1: Proceed as Planned**
- If todos properly extend lists/items
- TodoManagementService is correct
- No refactoring needed

**Option 2: Refactor to Align**
- If diverged from vision
- Use UniversalListRepository for todos
- Treat todos as Items with type="todo"
- Add todo-specific fields as extensions

**Option 3: Accept Divergence**
- If there's a good reason for separation
- Document the trade-off in an ADR
- Proceed with current approach

### D. Migration Path (if Option 2)

If refactoring is needed:
1. Can we adapt TodoRepository to use UniversalListRepository internally?
2. Or do we need to replace TodoRepository entirely?
3. What's the effort estimate?
4. Can we do it incrementally?

---

## Key Focus Areas

**Token Efficiency**: Use Serena's `find_symbol` and `analyze_relationship` commands rather than reading entire files.

**Look for**:
- Inheritance relationships (Todo extends Item?)
- Repository hierarchies
- Domain model definitions
- The word "universal" in todo-related code

**Don't spend time on**:
- Implementation details of the 17 methods
- UI or API layers
- Test files (unless they reveal design intent)

---

## Why This Matters

If we build TodoManagementService on the wrong foundation:
- We lock in architectural divergence
- Adding shopping lists, project backlogs becomes much harder
- We violate the PM's cognitive model of the domain
- Technical debt compounds quickly

Better to discover and fix now than after building more on top!

---

## Time Guidance

- 10 min: Explore generic system (UniversalList/Item)
- 10 min: Analyze todo implementation
- 10 min: Check relationships and compatibility
- 10 min: Form recommendation
- 5 min: Write clear report

**Remember**: We're not looking for perfect understanding, just enough to make an architectural decision.

Report back with findings and recommendation!
