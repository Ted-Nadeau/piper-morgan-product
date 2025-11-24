# Code Agent: Light Serena Investigation - Todo Persistence Architecture

## Mission

**Conduct a 30-45 minute architectural discovery** to inform Chief Architect's design decision on proper todo persistence. This is NOT about implementing - it's about discovering what exists and what patterns are already in use.

**Key Principle**: Archaeological discovery to inform (not constrain) architectural decisions.

---

## Investigation Questions

Answer these 5 questions using Serena's semantic code navigation:

### 1. What Todo-Related Code Currently Exists?

**Find**:
- All files/classes/functions related to todos
- What's implemented vs mocked
- What the structure looks like

**Serena Commands**:
```bash
# Find todo-related symbols
find_symbol todo

# Check TodoDB model
view services/database/models.py | grep -A 30 "class TodoDB"

# Check what exists in todo handlers
find_referencing_symbols TodoIntentHandlers

# Check API layer
view services/api/todo_management.py | head -100
```

**Document**:
- Where todo code lives
- What's complete vs incomplete
- Current architecture (if any)

### 2. What Persistence Patterns Exist Elsewhere?

**Find**: How do OTHER features persist to database?

**Example**: GitHub integration, if it exists
```bash
# Look for GitHub persistence
find_symbol github | grep -i "service\|repository\|db"

# Check how other features access database
grep -r "session.add" services/ --include="*.py" | head -20
grep -r "session.query" services/ --include="*.py" | head -20
```

**Document**:
- What patterns are used for database access?
- Direct DB access? Service layer? Repository pattern?
- Which approach is most common?

### 3. What Service Layer Patterns Are In Use?

**Find**: Existing service classes and their structure

```bash
# Find all service classes
find . -name "*service*.py" -type f | head -20

# Look at service structure
find_symbol Service | grep "class.*Service"

# Check TodoKnowledgeService
view services/todo/todo_knowledge_service.py

# Check other service examples
ls -la services/*/
```

**Document**:
- What service classes exist?
- What's their structure/responsibility?
- Do they handle database access?
- What patterns do they follow?

### 4. Any Repository Pattern Implementations?

**Find**: Repository classes if they exist

```bash
# Search for repository pattern
find_symbol repository
grep -r "class.*Repository" services/ --include="*.py"
find . -name "*repository*.py" -type f

# Check database directory structure
ls -la services/database/
view services/database/ | grep -E "\.py$"
```

**Document**:
- Does repository pattern exist?
- If so, where and how is it used?
- If not, how is database access abstracted?

### 5. How Does Database Session Management Work?

**Find**: Session factory and database access patterns

```bash
# Check session management
view services/database/session_factory.py

# See how sessions are used
grep -r "get_session" services/ --include="*.py" | head -20
grep -r "async with.*session" services/ --include="*.py" | head -10

# Check database models structure
view services/database/models.py | head -50
```

**Document**:
- How are database sessions created?
- What's the pattern for database access?
- Async? Context managers?
- Any transaction management?

---

## Investigation Protocol

### Time Limit: 45 minutes maximum

**Timebox each question**: ~9 minutes per question
**Focus on**: What exists, not what could exist
**Goal**: Facts for Chief Architect, not solutions

### Serena Usage Pattern

For each question:
1. Use `find_symbol` to locate relevant code
2. Use `view` to read key files
3. Use `grep` to find patterns
4. Use `find_referencing_symbols` to see usage

**Example workflow**:
```bash
# Find where TodoDB is used
find_symbol TodoDB
find_referencing_symbols TodoDB

# Look at a specific usage
view [file where TodoDB is used]

# Find similar patterns
grep -r "class.*DB" services/database/models.py
```

### What NOT to Do

- ❌ Don't implement anything
- ❌ Don't design solutions
- ❌ Don't spend more than 45 minutes
- ❌ Don't try to understand every detail
- ✅ DO get the big picture
- ✅ DO note patterns and approaches
- ✅ DO document what exists

---

## Reporting Format

Create a report with this structure:

```markdown
# Todo Persistence Architecture Discovery

**Investigation Date**: [date/time]
**Duration**: [actual time spent]
**Method**: Serena-enabled code navigation

---

## Question 1: What Todo-Related Code Exists?

**Findings**:
- [List files/classes/functions found]
- [Note what's implemented vs mocked]
- [Describe current structure]

**Evidence**:
- [Key file paths]
- [Notable symbols/functions]

---

## Question 2: Persistence Patterns Elsewhere

**Findings**:
- [What patterns are used in other features?]
- [Examples of database access]
- [Most common approach]

**Evidence**:
- [Example file/class showing pattern]
- [Grep results showing usage]

---

## Question 3: Service Layer Patterns

**Findings**:
- [What service classes exist?]
- [What's their structure?]
- [How do they handle data access?]

**Evidence**:
- [Example service class]
- [Pattern description]

---

## Question 4: Repository Pattern?

**Findings**:
- [Does it exist? Yes/No]
- [If yes, where and how?]
- [If no, what's used instead?]

**Evidence**:
- [Relevant files/classes]

---

## Question 5: Database Session Management

**Findings**:
- [How are sessions created?]
- [What's the access pattern?]
- [Transaction management approach?]

**Evidence**:
- [session_factory.py key details]
- [Example usage patterns]

---

## Summary for Chief Architect

**Current State**:
- [3-5 bullet points on what exists]

**Patterns in Use**:
- [2-3 patterns observed elsewhere]

**Key Observations**:
- [Any notable insights]

**Questions Raised**:
- [Anything unclear or inconsistent]
```

---

## Completion Criteria

- [ ] All 5 questions answered with evidence
- [ ] Report created in structured format
- [ ] Actual file paths and symbols documented
- [ ] Completed within 45 minutes
- [ ] No implementation attempted
- [ ] No solution design proposed
- [ ] Ready for Chief Architect review

---

## Where to Save Report

Save to: `dev/active/todo-persistence-architecture-discovery.md`

This will be included in Chief Architect consultation brief.

---

## Critical Reminders

**This is discovery, not design**:
- We're finding what exists
- Not proposing what should exist
- Chief Architect will design the solution
- Our job is to provide facts

**Speed over perfection**:
- 45 minutes is enough
- Don't need to understand everything
- Get the patterns and structure
- Details can come later

**Focus on patterns**:
- How do things work NOW?
- What patterns are ALREADY in use?
- What exists that we can learn from?
- What's the current architectural approach?

---

## Start Investigation Now

Begin with Question 1, spend ~9 minutes per question, document findings as you go.

Report back when complete with the discovery document.

Good luck! 🏰
