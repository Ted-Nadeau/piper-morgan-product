# Internal Documentation Navigation Hub

**Purpose**: Internal development team navigation for restructured documentation
**Audience**: Agents, developers, architects, and internal contributors
**Public Documentation**: See [README.md](README.md) for pmorgan.tech public site

**Last Updated**: October 27, 2025
**Status**: ✅ **Complete Internal Navigation System** - Role-based access for development teams

---

> **Note**: This navigation serves **internal development workflows**. For public project information, getting started guides, and user documentation, visit the main [README.md](README.md) which powers the pmorgan.tech website.

---

## 🚀 Quick Start by Role

### Essential Briefings (Start Here)

- [Lead Developer](../knowledge/BRIEFING-ESSENTIAL-LEAD-DEV.md) - 2.5K tokens
- [Chief Architect](../knowledge/BRIEFING-ESSENTIAL-ARCHITECT.md) - 2.5K tokens
- [Chief of Staff](../knowledge/BRIEFING-ESSENTIAL-CHIEF-STAFF.md) - 2.5K tokens
- [Communications](../knowledge/BRIEFING-ESSENTIAL-COMMS.md) - 2.5K tokens
- [Coding Agent](../knowledge/BRIEFING-ESSENTIAL-AGENT.md) - 2K tokens
- [LLM Support](../knowledge/BRIEFING-ESSENTIAL-LLM.md) - 1K tokens

### Progressive Loading

Each essential briefing includes triggers for loading detailed documentation as needed.

---

## 🧭 Quick Navigation by Role

### 👨‍💼 Product Managers

- **[Current Planning](internal/planning/current/)** - Active planning cycles and roadmaps
- **[Issue Tracking](internal/planning/current/issues.csv)** - Current PM issue status
- **[Roadmap](internal/planning/roadmap/)** - Strategic planning and milestones
- **[Backlog Management](internal/planning/current/)** - Priority management and organization

### 🏗️ Architects

- **[Architecture Hub](internal/architecture/current/)** - Current architectural decisions
- **[Domain Models](internal/architecture/current/models/)** - Hub-and-spoke model documentation
- **[ADRs](internal/architecture/current/adrs/)** - Architectural Decision Records
- **[Patterns](internal/architecture/current/patterns/)** - Established architectural patterns
- **[Technical Evolution](internal/architecture/evolution/)** - Architecture development history

### 👨‍💻 Developers

- **[Development Tools](internal/development/tools/)** - Setup guides and development workflows
- **[Active Work](internal/development/active/)** - Current development status
- **[Methodology](internal/development/methodology-core/)** - Development methodologies (20 core patterns)
- **[Methodology Index](internal/development/methodology-core/INDEX.md)** - Comprehensive methodology navigation
- **[Handoffs](internal/development/handoffs/)** - Agent coordination protocols
- **[Session Templates](internal/development/tools/session-log-templates/)** - Session documentation

### 📚 Researchers & Historians

- **[Session Logs Archive](dev/2025/)** - Chronological development history (dev/2025/MM/DD/ structure)
- **[Omnibus Logs](omnibus-logs/)** - Weekly/monthly session consolidations
- **[Development Logs](internal/development/active/)** - Active development work and status files

### 👥 External Users

- **[Getting Started](public/getting-started/)** - Public onboarding materials
- **[API Reference](public/api-reference/)** - Public API documentation
- **[User Guides](public/user-guides/)** - End-user documentation

---

## 📁 Documentation Architecture

### 🔓 Public Documentation (`public/`)

**External-facing content for users and developers**

- Getting started guides and tutorials
- API documentation and references
- User manuals and help content

### 🔒 Internal Documentation (`internal/`)

**Working documents for active development**

#### Development (`internal/development/`)

```
├── active/                    # Current work by status
│   ├── in-progress/          # Active development
│   ├── pending-review/       # Files needing review
│   └── ready-for-integration/ # Completed work
├── methodology-core/         # 20 development methodologies (see INDEX.md)
├── tools/                    # Development tools and guides
├── handoffs/                 # Agent coordination prompts
└── planning/                 # Current planning cycles
```

#### Architecture (`internal/architecture/`)

```
├── current/                   # Active architectural decisions
│   ├── models/               # Hub-and-spoke model docs (39 models)
│   ├── adrs/                 # Current ADRs
│   ├── patterns/             # Established patterns
│   └── [core-specs]          # API, technical specifications
├── evolution/                # Architectural evolution tracking
└── decisions/                # Decision logs and rationale
```

## Architecture Patterns

- [Pattern-031: Plugin Wrapper](internal/architecture/current/patterns/pattern-031-plugin-wrapper.md) - Adapter pattern for integration routers

## Developer Guides

- [Plugin Development Guide](guides/plugin-development-guide.md) - Step-by-step tutorial for adding integrations
- [Plugin Versioning Policy](guides/plugin-versioning-policy.md) - Semantic versioning guidelines for plugins
- [Plugin Quick Reference](guides/plugin-quick-reference.md) - Cheat sheet for common tasks
- [Intent Classification Guide](guides/intent-classification-guide.md) - Universal intent enforcement developer guide
- [User Context Service](guides/user-context-service.md) - Multi-user context architecture guide
- [Canonical Handlers Architecture](guides/canonical-handlers-architecture.md) - Handler design and capabilities
- [EXECUTION/ANALYSIS Handlers](guides/execution-analysis-handlers.md) - Intent routing to domain services

## Examples

- [Demo Plugin](../services/integrations/demo/) - Complete example integration to copy and adapt

#### Planning (`internal/planning/`)

```
├── current/                  # Active planning cycle
│   ├── data/                 # Planning data and analysis
│   ├── draft-issues/         # Issue development
│   ├── editorial/            # Content planning
│   └── integration/          # Integration planning
├── roadmap/                  # Long-term strategic planning
└── historical/               # Previous planning cycles
```

### 📚 Knowledge Base (`knowledge/`)

**Staging area for claude.ai project knowledge**

Files optimized for RAG search in the claude.ai project knowledge base:
- **BRIEFING-*** files use prefix for context in flat namespace
- **Symlinked canonical sources** from docs/briefing/ (zero duplication)
- **Workflow**: Update files in docs/briefing/ → automatically syncs to knowledge/ → PM updates claude.ai

```
knowledge/
├── BRIEFING-CURRENT-STATE.md        → Symlink to docs/briefing/
├── BRIEFING-ESSENTIAL-LEAD-DEV.md   → Symlink to docs/briefing/
├── BRIEFING-ESSENTIAL-ARCHITECT.md  → Symlink to docs/briefing/
├── BRIEFING-ESSENTIAL-AGENT.md      → Symlink to docs/briefing/
├── BRIEFING-ESSENTIAL-*.md          → Symlinks to docs/briefing/
├── CLAUDE.md                        # Agent entry point
├── serena-briefing-queries.md       # Live system state queries
└── README.md                        # Knowledge base workflow guide
```

**See**: `knowledge/README.md` for complete workflow documentation

### 📦 Archives (`archives/`)

**Historical preservation and archaeological research**

#### Session Logs (`archives/session-logs/`)

```
├── 2025/                     # Chronological by year
│   ├── 05/ (May logs)
│   ├── 06/ (June logs)
│   ├── 07/ (July logs)
│   ├── 08/ (August logs)
│   └── 09/ (September logs + index.md)
├── omnibus-logs/             # 102+ weekly/monthly consolidations
└── yearly-index.md           # High-level research navigation
```

#### Artifacts & Decisions (`archives/`)

- **Artifacts**: Generated reports, PM files, historical deliverables
- **Decisions**: Completed ADRs and historical planning decisions

### 🎨 Assets (`assets/`)

**Binary files and multimedia content with size management**

```
├── images/                   # Organized by purpose
│   ├── architecture/         # System diagrams
│   ├── screenshots/          # Development captures
│   └── blog/                 # Blog content (186+ files)
├── diagrams/                 # Source and generated
│   ├── source/               # Editable formats
│   └── generated/            # PNG/SVG outputs
└── documents/                # Templates and exports
    ├── templates/            # Document boilerplates
    └── exports/              # Generated documentation
```

---

## 🔍 Finding What You Need

### By Work Type

- **Current Tasks**: `internal/development/active/`
- **Strategic Planning**: `internal/planning/current/`
- **Technical Decisions**: `internal/architecture/current/`
- **Historical Research**: `archives/session-logs/`
- **Asset Management**: `assets/` with inventory and guidelines

### By Time Period

- **Today's Work**: Check `internal/` directories for current status
- **Recent History**: `archives/session-logs/2025/09/`
- **Project History**: `archives/session-logs/yearly-index.md`
- **Decision Evolution**: `internal/architecture/evolution/`
- **Weekly Insights**: `archives/session-logs/omnibus-logs/`

### By Content Type

- **Documentation**: Start with role-based navigation above
- **Code References**: `internal/architecture/current/models/`
- **Processes**: `internal/development/methodology-core/`
- **Images/Assets**: `assets/` with inventory in README
- **Historical Deliverables**: `archives/artifacts/`

---

## 🔧 Documentation Workflow

### For Daily Work

1. **Check active status** in relevant `internal/` directory
2. **Review methodology** for process guidance
3. **Create session artifacts** in local `dev/YYYY/MM/DD/` structure
4. **Process to archives** for permanent preservation

### For Research & Investigation

1. **Start with yearly index** for time-based research
2. **Use monthly indices** for detailed period investigation
3. **Cross-reference artifacts** with session logs
4. **Follow agent collaboration** patterns and handoffs
5. **Check omnibus logs** for strategic insights

### For New Content Creation

1. **Determine audience** (public, internal, or archive)
2. **Follow asset guidelines** for binary files
3. **Update navigation** as needed for major additions
4. **Maintain cross-references** between related content

---

## 📊 Restructuring Achievement Summary

### Transformation Completed (September 20, 2025)

- **787 files surveyed** across 104 directories
- **6-phase systematic restructuring** with zero data loss
- **Session log consolidation** with archaeological optimization
- **186+ binary files organized** with size management
- **Role-based navigation** for multiple user types

### Key Organizational Improvements

- ✅ **Clear active/historical separation** across all content types
- ✅ **Session-based archaeological research** with chronological navigation
- ✅ **Asset management** with size compliance and inventory tracking
- ✅ **Multi-role navigation** supporting different user needs
- ✅ **Archaeological research enhancement** with cross-referencing

### Performance Metrics

- **Phase 1**: Foundation architecture (15 min vs 30 min planned)
- **Phase 2**: Session log consolidation (20 min vs 45 min planned)
- **Phase 3**: Development restructuring (45 min vs 60 min planned)
- **Phase 4**: Architecture optimization (20 min vs 30 min planned)
- **Phase 5**: Asset organization (25 min vs 30 min planned)
- **Phase 6**: Navigation system (15 min vs 30 min planned)
- **Total**: 2 hours 20 minutes vs 3.5 hours planned

---

## 🚀 Quick Access Links

### Most Frequently Used

- **[September 2025 Session Logs](archives/session-logs/2025/09/index.md)** - Current month activities
- **[Active Development Work](internal/development/active/)** - What's happening now
- **[Domain Models Hub](internal/architecture/current/models/models-architecture.md)** - Complete model reference
- **[Methodology Core](internal/development/methodology-core/INDEX.md)** - Development patterns and processes

### For New Team Members

- **[Public Getting Started](public/getting-started/)** - External onboarding
- **[Development Tools](internal/development/tools/)** - Developer setup and guides
- **[Architecture Overview](internal/architecture/current/)** - System understanding
- **[Historical Context](archives/session-logs/yearly-index.md)** - Project evolution

### For Research & Analysis

- **[Omnibus Logs](archives/session-logs/omnibus-logs/)** - Strategic insights and weekly summaries
- **[Decision Archive](archives/decisions/)** - Historical decision context
- **[Agent Coordination](internal/development/handoffs/)** - Multi-agent collaboration patterns
- **[Archaeological Index](archives/session-logs/yearly-index.md)** - Complete research navigation

---

## 🆘 Help and Support

### Navigation Issues

- **Can't find specific content?** Check role-based quick navigation above
- **Looking for historical material?** Start with `archives/session-logs/yearly-index.md`
- **Need methodology guidance?** Review `internal/development/methodology-core/`
- **Asset questions?** Check `assets/README.md` and `assets/INVENTORY.md`

### Contributing to Documentation

- **Follow organization principles** established in restructuring
- **Maintain archaeological research** capability in changes
- **Use asset guidelines** in `assets/README.md`
- **Update navigation** when adding major new sections

---

_Comprehensive navigation system established: September 20, 2025_
_Supporting role-based access to restructured documentation architecture_
