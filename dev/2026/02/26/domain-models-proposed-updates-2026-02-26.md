# Proposed Updates to domain-models.md

**From**: Principal Product Manager
**Date**: February 26, 2026
**Re**: Aligning domain-models.md with PDR-003 Entity Concept Model

---

## Current State

**Last Updated**: January 21, 2026 (MUX-TECH X1 Sprint)
**Key Issues Identified**:

1. **Repository is missing entirely** — not listed as a first-class entity
2. **Product vs Project confusion** — definitions overlap, inheritance relationship unclear
3. **No explicit Product ↔ Project relationship** — both exist but aren't linked
4. **ProjectIntegration contains repo config** — should be migrated to Repository entity

---

## Proposed Changes

### 1. Add Repository to Quick Reference

**Current** (missing):
```
(Repository not listed)
```

**Proposed**:
```markdown
### Core Business Models

- [Product](#product) - Products being managed (the thing you ship)
- [Project](#project) - PM projects/workstreams (bounded efforts)
- [Repository](#repository) - Code repositories (NEW - first-class entity)
- [Feature](#feature) - Features or capabilities
- [WorkItem](#workitem) - Universal work items from any system
- [Stakeholder](#stakeholder) - People with interest in products
```

### 2. Clarify Product Definition

**Current**:
```markdown
### Product

**Purpose**: A product being managed

@dataclass
class Product:
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    vision: str = ""
    strategy: str = ""
    ...
```

**Proposed**:
```markdown
### Product

**Purpose**: The thing you're building and shipping — the whole that users/customers experience.

**User mental model**: "My product is Piper Morgan" or "My products are the iOS and Android apps"

**Relationship to Project**: Many-to-many. A Product may have multiple Projects contributing to it; a Project may serve multiple Products (e.g., platform work).

@dataclass
class Product:
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    vision: str = ""
    strategy: str = ""
    owner_id: str = ""  # User who owns this product
    is_default: bool = False  # Primary product for this user
    is_archived: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    # Relationships
    projects: List["Project"] = field(default_factory=list)  # NEW - many-to-many
    features: List["Feature"] = field(default_factory=list)
    stakeholders: List["Stakeholder"] = field(default_factory=list)
    metrics: List["Metric"] = field(default_factory=list)
    work_items: List["WorkItem"] = field(default_factory=list)
```

### 3. Clarify Project Definition (Remove Inheritance)

**Current**:
```markdown
### Project

**Purpose**: A PM project with multiple tool integrations

**Updates (Phase 3 SEC-RBAC)**:
- Added `owner_id` field...

@dataclass
class Project:
    id: str = field(default_factory=lambda: str(uuid4()))
    owner_id: str = ""
    name: str = ""
    description: str = ""
    integrations: List[ProjectIntegration] = field(default_factory=list)
    ...
```

**Proposed**:
```markdown
### Project

**Purpose**: A bounded effort with intent — a workstream, release, feature initiative, or epic.

**User mental model**: "The Q1 release" or "The authentication overhaul" or "M0 sprint"

**Relationship to Product**: Many-to-many. A Project may contribute to multiple Products; a Product may have multiple Projects.

**Relationship to Repository**: Many-to-many. A Project may use multiple Repositories; a Repository may serve multiple Projects.

> ⚠️ **Note**: Project does NOT inherit from Product. They are distinct concepts with a many-to-many relationship. See PDR-003 for rationale.

@dataclass
class Project:
    id: str = field(default_factory=lambda: str(uuid4()))
    owner_id: str = ""
    name: str = ""
    description: str = ""
    is_default: bool = False
    is_archived: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    # Relationships
    products: List["Product"] = field(default_factory=list)  # NEW - many-to-many
    repositories: List["Repository"] = field(default_factory=list)  # NEW - many-to-many
    integrations: List[ProjectIntegration] = field(default_factory=list)  # Non-repo integrations
    shared_with: List[SharePermission] = field(default_factory=list)
```

### 4. Add New Repository Entity

**Current**: (Does not exist)

**Proposed** (add new section):
```markdown
### Repository

**Purpose**: A code repository — where code lives. First-class entity independent of Projects.

**User mental model**: "The frontend repo" or "the monorepo" or "the shared components library"

**Relationship to Project**: Many-to-many. A Repository may serve multiple Projects; a Project may use multiple Repositories.

> 📋 **Migration Note**: Repository data previously stored in `ProjectIntegration.config` for GitHub integrations should be migrated to this entity. See PDR-003 for migration strategy.

@dataclass
class Repository:
    """A code repository — first-class entity"""
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""  # Display name (e.g., "Platform Repo")
    url: str = ""  # Full URL (e.g., "https://github.com/org/repo")
    provider: str = "github"  # github, gitlab, bitbucket
    default_branch: str = "main"
    owner_id: str = ""  # User who connected this repo
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    # Sync state
    last_synced_at: Optional[datetime] = None
    sync_status: str = "pending"  # pending, syncing, synced, error

    # Relationships
    projects: List["Project"] = field(default_factory=list)
```

### 5. Update ProjectIntegration (Deprecate Repo Config)

**Current**:
```markdown
### ProjectIntegration

**Purpose**: Configuration for external system integrations.

@dataclass
class ProjectIntegration:
    id: str = field(default_factory=lambda: str(uuid4()))
    type: IntegrationType
    name: str = ""
    config: Dict[str, Any] = field(default_factory=dict)  # Contains repo URL for GitHub
    ...
```

**Proposed**:
```markdown
### ProjectIntegration

**Purpose**: Configuration for non-repository external system integrations (Slack, Calendar, Jira, etc.).

> ⚠️ **Deprecation Note**: GitHub repository configuration previously stored in `config` has been migrated to the `Repository` entity. ProjectIntegration should no longer be used for repository connections. See PDR-003.

@dataclass
class ProjectIntegration:
    id: str = field(default_factory=lambda: str(uuid4()))
    type: IntegrationType  # Excludes GITHUB for new integrations
    name: str = ""
    config: Dict[str, Any] = field(default_factory=dict)
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    project_id: Optional[str] = None

    # Relationships
    project: Optional["Project"] = None
```

### 6. Add Relationship Diagram Section

**Current**: (Does not exist as clear visual)

**Proposed** (add new section):
```markdown
## Entity Relationships

### Core Entity Graph

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│   Product   │◄─────►│   Project   │◄─────►│ Repository  │
│             │ M:N   │             │ M:N   │             │
│ - vision    │       │ - scope     │       │ - url       │
│ - strategy  │       │ - timeline  │       │ - provider  │
│ - roadmap   │       │ - team      │       │ - branch    │
└─────────────┘       └─────────────┘       └─────────────┘
      │                     │
      │ 1:N                 │ 1:N
      ▼                     ▼
┌─────────────┐       ┌─────────────┐
│   Feature   │       │ Integration │
│             │       │ (non-repo)  │
└─────────────┘       └─────────────┘
```

### Cardinality Rules

| Relationship | Cardinality | Join Table |
|--------------|-------------|------------|
| Product ↔ Project | Many-to-Many | `product_projects` |
| Project ↔ Repository | Many-to-Many | `project_repositories` |
| Product → Feature | One-to-Many | FK on Feature |
| Project → Integration | One-to-Many | FK on Integration |

### Key Principle

**Products emerge from Projects, not the other way around.**

Users start with Projects (the concrete work). Products (the organizational container) emerge as users recognize patterns. See PDR-003 for UX surfacing strategy.
```

### 7. Update Recent Updates Section

**Current**:
```markdown
## Recent Updates (January 21, 2026)

### MUX-TECH X1 Sprint - Consciousness and Ownership Models
...
```

**Proposed** (add new entry):
```markdown
## Recent Updates (February 26, 2026)

### PDR-003: Entity Concept Model — Product, Project, Repository

**Major architectural changes**:

1. **Repository promoted to first-class entity**
   - New `Repository` dataclass added
   - Many-to-many relationship with Project via `project_repositories` join table
   - Migrates repo config out of ProjectIntegration

2. **Product ↔ Project relationship formalized**
   - Many-to-many via `product_projects` join table
   - Removes confusing inheritance (`Project extends Product`)
   - Clear concept separation: Product = what you ship, Project = work you do

3. **ProjectIntegration scoped to non-repo integrations**
   - GitHub repo config deprecated in favor of Repository entity
   - Remains valid for Slack, Calendar, Jira, etc.

**New fields added**:
- `Product.owner_id`, `Product.is_default`, `Product.is_archived`
- `Product.projects` (relationship)
- `Project.products`, `Project.repositories` (relationships)
- `Repository` (entire new entity)

**References**: PDR-003, #848, #861

---

## Recent Updates (January 21, 2026)
...
```

---

## Summary of Changes

| Section | Change Type | Description |
|---------|-------------|-------------|
| Quick Reference | Add | Repository to Core Business Models |
| Product | Update | Clarify definition, add relationships |
| Project | Update | Remove inheritance, add relationships |
| Repository | Add | Entire new section |
| ProjectIntegration | Update | Deprecation note for repo config |
| Entity Relationships | Add | New diagram and cardinality rules |
| Recent Updates | Add | February 26, 2026 entry |

---

## Implementation Notes

These documentation changes should be made **after** the domain model code changes are implemented. The sequence:

1. Lead Dev implements Repository entity + migrations
2. Lead Dev implements Product ↔ Project join table
3. Documentation updated to reflect new reality
4. PDR-003 status changed from DRAFT to APPROVED

---

*Proposed by PPM, February 26, 2026*
